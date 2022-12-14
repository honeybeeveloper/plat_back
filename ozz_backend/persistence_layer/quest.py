from sqlalchemy.orm import aliased

from ozz_backend.database import entity
from ozz_backend.database.conn import DBSession


class Quest(object):
    @staticmethod
    def get_quest_with_mission_id(mission_id):
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
                               entity.QuestBridgeTb.quest_cd,
                               entity.QuestBridgeTb.quest_order,
                               entity.QuestBridgeTb.link_quest_id) \
            .join(entity.QuestBridgeTb, entity.QuestTB.id == entity.QuestBridgeTb.quest_id)\
            .filter(entity.QuestBridgeTb.mission_id == mission_id).subquery()
        sub_query = aliased(stmt, name='sub_query')

        return DBSession.query(sub_query.c.id, sub_query.c.quest_name, sub_query.c.description,
                               sub_query.c.thumbnail_path, sub_query.c.quest_cd, sub_query.c.quest_order,
                               sub_query.c.link_quest_id, entity.QuestBridgeTb.quest_cd.label('link_quest_cd'))\
            .outerjoin(entity.QuestBridgeTb, sub_query.c.link_quest_id == entity.QuestBridgeTb.id)\
            .order_by(sub_query.c.quest_order).all()
