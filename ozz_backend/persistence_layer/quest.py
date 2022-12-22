from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.orm import aliased

from ozz_backend import app_logger
from ozz_backend.common.exception import FailToUpdate, ValueNotFoundEx, FailToInsertion
from ozz_backend.database import entity
from ozz_backend.database.conn import DBSession


class Quest(object):
    @staticmethod
    def get_quests_with_mission_id(mission_id):
        # query-1
        # select
        #     qt.id, qt.quest_name, qt.description, qt.thumbnail_path,
        #     qbt.quest_cd, qbt.quest_order, qbt.link_quest_id,
        #     (select quest_cd from quest_bridge_tb qbt2 where id = qbt.link_quest_id) as link_quest_cd
        # from quest_tb qt inner join quest_bridge_tb qbt
        #     on qt.id = qbt.quest_id
        # where qbt.mission_id = :mission_id
        # order by qbt.quest_order;

        #query-2
        # select
        #     qt.id, qt.quest_name, qt.description, qt.thumbnail_path,
        #     qbt.quest_cd, qbt.quest_order, qbt.link_quest_id, qbt2.quest_cd as link_quest_cd
        # from quest_tb qt
        #     inner join quest_bridge_tb qbt
        #         on qt.id = qbt.quest_id
        #     left outer join quest_bridge_tb qbt2
        #         on qbt2.id = qbt.link_quest_id
        # where qbt.mission_id = :mission_id
        # order by qbt.quest_order;

        # TODO : check query performance or orm usage
        stmt = DBSession.query(entity.QuestTB.id,
                               entity.QuestTB.quest_name,
                               entity.QuestTB.description,
                               entity.QuestTB.thumbnail_path,
                               entity.QuestBridgeTB.quest_cd,
                               entity.QuestBridgeTB.quest_order,
                               entity.QuestBridgeTB.link_quest_id) \
            .join(entity.QuestBridgeTB, entity.QuestTB.id == entity.QuestBridgeTB.quest_id)\
            .filter(entity.QuestBridgeTB.mission_id == mission_id).subquery()
        sub_query = aliased(stmt, name='sub_query')

        return DBSession.query(sub_query.c.id, sub_query.c.quest_name, sub_query.c.description,
                               sub_query.c.thumbnail_path, sub_query.c.quest_cd, sub_query.c.quest_order,
                               sub_query.c.link_quest_id, entity.QuestBridgeTB.quest_cd.label('link_quest_cd'))\
            .outerjoin(entity.QuestBridgeTB, sub_query.c.link_quest_id == entity.QuestBridgeTB.id)\
            .order_by(sub_query.c.quest_order).all()

    @staticmethod
    def get_quest_with_mission_id_quest_order(mission_id, quest_order):
        try:
            quest_info = DBSession.query(entity.QuestBridgeTB.quest_id,
                                         entity.QuestBridgeTB.quest_cd,
                                         entity.QuestBridgeTB.quest_order)\
                            .filter(entity.QuestBridgeTB.mission_id == mission_id)\
                            .filter(entity.QuestBridgeTB.quest_order == quest_order).one()
            return quest_info
        except NoResultFound as e:
            app_logger.error(e)
            raise ValueNotFoundEx('quest info not found')

    @staticmethod
    def add_user_quest_log(data):
        try:
            DBSession.add(entity.UserQuestLogTB(user_id=data.user_id,
                                                mission_id=data.mission_id,
                                                quest_id=data.quest_id,
                                                status=data.status))
            DBSession.commit()
        except SQLAlchemyError as e:
            app_logger.error(e)
            raise FailToInsertion('fail to insert into user_quest_log_tb')

    @staticmethod
    def modify_user_quest_log(data):
        try:
            now = datetime.now()
            DBSession.query(entity.UserQuestLogTB)\
                .filter(entity.UserQuestLogTB.user_id == data.user_id)\
                .filter(entity.UserQuestLogTB.mission_id == data.mission_id) \
                .filter(entity.UserQuestLogTB.quest_id == data.quest_id) \
                .update({'status': data.status, 'modified_at': now})
            DBSession.commit()
        except SQLAlchemyError as e:
            app_logger.error(e)
            raise FailToUpdate('fail to update user_quest_log_tb')

    @staticmethod
    def get_quest_order(mission_id, quest_id):
        try:
            DBSession.query(entity.QuestBridgeTB.quest_order) \
                .filter(entity.QuestBridgeTB.mission_id == mission_id)\
                .filter(entity.QuestBridgeTB.quest_id == quest_id)\
                .filter(entity.QuestBridgeTB.mission_id == entity.UserQuestLogTB.mission_id)\
                .filter(entity.QuestBridgeTB.quest_id == entity.UserQuestLogTB.quest_id)\
                .one()
        except NoResultFound as e:
            app_logger.error(e)
            raise ValueNotFoundEx('quest order info not found')

