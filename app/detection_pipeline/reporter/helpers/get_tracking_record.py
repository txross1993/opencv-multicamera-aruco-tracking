from detection_pipeline.event_struct.aruco_tag_event_struct import TagEventStruct
from database_conn.schema_definitions.table_loader import TableLoader

class TagEventRecord:

    def setTrackingTable(self, tracking_tbl):
        TagEventRecord.RackTracking = TableLoader().get_table_class(tracking_tbl)
    
    def setTrackingTableColumns(self):
        TagEventRecord._columns = TableLoader().get_columns(TagEventRecord.RackTracking)

    def getRecord(self, event:TagEventStruct):
        attr_map = self.assert_column_data_types(event)

        Rack =  TagEventRecord.RackTracking(tagId=attr_map['tagId'],
                                            streamStreamId=attr_map['streamStreamId'],
                                            ts=attr_map['ts'],
                                            roomCoordX=attr_map['roomCoordX'],
                                            roomCoordY=attr_map['roomCoordY'])

        return Rack
    
    def assert_column_data_types(self, event):
        attr_map = {
            'tagId': event.tagId,
            'streamStreamId': event.sourceStream,
            'ts': event.timestamp,
            'roomCoordX': event.location.x,
            'roomCoordY': event.location.y

        }
        for column_name, column_type in TagEventRecord._columns.items():
            attr_map[column_name] = column_type(attr_map[column_name])
        
        return attr_map
            

        