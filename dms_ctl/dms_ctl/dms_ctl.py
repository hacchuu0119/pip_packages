from time import sleep
from datetime import timezone, datetime, timedelta


def create_timestamp():
    jst = timezone(timedelta(hours=+9), 'JST')
    execute_time = datetime.now(jst)
    return f'{execute_time.year}{execute_time.month}{execute_time.day}{execute_time.hour}{execute_time.minute}'


def create_filter_dic(filter_name, filter_values):
    if type(filter_values) is not list:
        filter_values = [filter_values]

    return {'Name': filter_name,
            'Values': filter_values}


class DMSCtl:
    def __init__(self, boto3_session):
        self.dms_client = boto3_session.client('dms')

        self.timestamp = create_timestamp()

    def delete_replication_task(self, replication_task_arn):
        try:
            response = self.dms_client.delete_replication_task(
                ReplicationTaskArn=replication_task_arn
            )

        except:
            print("faild: delete replication task")
            raise

        return response

    def create_replication_task(self,
                                task_name,
                                source_endpoint_arn,
                                target_endpoint_arn,
                                replication_instance_arn,
                                table_mapping_json,
                                migration_type='full-load-and-cdc'):

        try:
            response = self.dms_client.create_replication_task(
                ReplicationTaskIdentifier=f'{task_name}-{self.timestamp}',
                SourceEndpointArn=source_endpoint_arn,
                TargetEndpointArn=target_endpoint_arn,
                ReplicationInstanceArn=replication_instance_arn,
                MigrationType=migration_type,
                TableMappings=table_mapping_json
            )
        except:
            print("faild: create replication task")
            raise

        return response

    def get_replication_task_status(self, filter_dic, *args):
        """
        The name is one of the following:
        replication-task-arn | replication-task-id | migration-type | endpoint-arn | replication-instance-arn
        """

        filters = list(args)
        filters.append(filter_dic)

        response = self.dms_client.describe_replication_tasks(
            Filters=filters
        )

        return response['ReplicationTasks']

    def get_endpoint_status(self, filter_dic, *args):
        """
        The name is one of the following:
        endpoint-arn | endpoint-type | endpoint-id | engine-name
        """

        filters = list(args)
        filters.append(filter_dic)

        response = self.dms_client.describe_endpoints(
            Filters=filters
        )

        return response['Endpoints']

    def get_task_status_from_endpoint(self, source_endpoint_name, target_endpoint_name):

        source_endpoint_arn = self.get_endpoint_status(create_filter_dic('endpoint-id',
                                                                         source_endpoint_name))[0]['EndpointArn']

        target_endpoint_arn = self.get_endpoint_status(create_filter_dic('endpoint-id',
                                                                         target_endpoint_name))[0]['EndpointArn']

        task_response = self.get_replication_task_status(create_filter_dic('endpoint-arn',
                                                                           [source_endpoint_arn,
                                                                            target_endpoint_arn]))

        for task_status in task_response:
            if task_status['SourceEndpointArn'] == source_endpoint_arn and \
                    task_status['TargetEndpointArn'] == target_endpoint_arn:
                return task_status

    def recreate_replication_task(self, source_endpoint_name, target_endpoint_name):
        task_status = self.get_task_status_from_endpoint(source_endpoint_name, target_endpoint_name)

        task_arn = task_status['ReplicationTaskArn']
        print(task_arn)

        # 開始している場合終了処理
        if self.get_replication_task_status(create_filter_dic('replication-task-arn',
                                                              task_arn))[0]['Status'] == 'running' and \
                self.get_replication_task_status(create_filter_dic('replication-task-arn',
                                                                   task_arn))[0]['Status'] == 'starting':
            self.dms_client.stop_replication_task(ReplicationTaskArn=task_arn)
            self._wait_replication_task_status(task_arn, 'stopped')

        delete_task_details = self.delete_replication_task(task_arn)['ReplicationTask']
        print(delete_task_details)
        # self._wait_delete_replication_task(task_arn)

        create_task_status = self.create_replication_task(
            '-'.join(delete_task_details['ReplicationTaskIdentifier'].split('-')[:-1]),
            delete_task_details['SourceEndpointArn'],
            delete_task_details['TargetEndpointArn'],
            delete_task_details['ReplicationInstanceArn'],
            delete_task_details['TableMappings']
        )

        new_task_arn = create_task_status['ReplicationTask']['ReplicationTaskArn']

        self._wait_replication_task_status(new_task_arn, 'ready')

        self.start_replication_task(new_task_arn)

    def _wait_replication_task_status(self, repl_task_arn, target_status):

        repl_task_filter = create_filter_dic('replication-task-arn', repl_task_arn)

        task_status = self.get_replication_task_status(repl_task_filter)[0]['Status']
        wait_s = 0

        while task_status != target_status:
            print(f'Changing...  Status[{self.get_replication_task_status(repl_task_filter)[0]["Status"]}]  ', end='')
            sleep(30)
            wait_s += 30
            print(f'{wait_s}s Elapsed.')
            task_status = self.get_replication_task_status(repl_task_filter)[0]['Status']
        print('Changed!...  Wait last 30 minutes!')
        sleep(30)

    def _wait_delete_replication_task(self, task_arn):
        wait_s = 0
        try:
            while True:
                self.get_replication_task_status(create_filter_dic('replication-task-arn', task_arn))
                print('Deleating... ', )
                sleep(30)
                wait_s += 30
                print(f'{wait_s}s Elapsed')
        finally:
            return

    def start_replication_task(self, replication_task_arn, task_type='reload-target'):
        try:
            response = self.dms_client.start_replication_task(
                ReplicationTaskArn=replication_task_arn,
                StartReplicationTaskType=task_type
            )
        except:
            print('faild: start replication task')
            raise

        return response
