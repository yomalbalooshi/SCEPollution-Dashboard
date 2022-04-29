"""
Type annotations for timestream-query service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_timestream_query.client import TimestreamQueryClient

    session = Session()
    client: TimestreamQueryClient = session.client("timestream-query")
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, Mapping, Sequence, Type, Union, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ScheduledQueryStateType
from .paginator import ListScheduledQueriesPaginator, ListTagsForResourcePaginator, QueryPaginator
from .type_defs import (
    CancelQueryResponseTypeDef,
    CreateScheduledQueryResponseTypeDef,
    DescribeEndpointsResponseTypeDef,
    DescribeScheduledQueryResponseTypeDef,
    ErrorReportConfigurationTypeDef,
    ListScheduledQueriesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    NotificationConfigurationTypeDef,
    PrepareQueryResponseTypeDef,
    QueryResponseTypeDef,
    ScheduleConfigurationTypeDef,
    TagTypeDef,
    TargetConfigurationTypeDef,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("TimestreamQueryClient",)


class BotocoreClientError(BaseException):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidEndpointException: Type[BotocoreClientError]
    QueryExecutionException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class TimestreamQueryClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TimestreamQueryClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#can_paginate)
        """

    def cancel_query(self, *, QueryId: str) -> CancelQueryResponseTypeDef:
        """
        Cancels a query that has been issued.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.cancel_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#cancel_query)
        """

    def create_scheduled_query(
        self,
        *,
        Name: str,
        QueryString: str,
        ScheduleConfiguration: "ScheduleConfigurationTypeDef",
        NotificationConfiguration: "NotificationConfigurationTypeDef",
        ScheduledQueryExecutionRoleArn: str,
        ErrorReportConfiguration: "ErrorReportConfigurationTypeDef",
        TargetConfiguration: "TargetConfigurationTypeDef" = ...,
        ClientToken: str = ...,
        Tags: Sequence["TagTypeDef"] = ...,
        KmsKeyId: str = ...
    ) -> CreateScheduledQueryResponseTypeDef:
        """
        Create a scheduled query that will be run on your behalf at the configured
        schedule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.create_scheduled_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#create_scheduled_query)
        """

    def delete_scheduled_query(self, *, ScheduledQueryArn: str) -> None:
        """
        Deletes a given scheduled query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.delete_scheduled_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#delete_scheduled_query)
        """

    def describe_endpoints(self) -> DescribeEndpointsResponseTypeDef:
        """
        DescribeEndpoints returns a list of available endpoints to make Timestream API
        calls against.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.describe_endpoints)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#describe_endpoints)
        """

    def describe_scheduled_query(
        self, *, ScheduledQueryArn: str
    ) -> DescribeScheduledQueryResponseTypeDef:
        """
        Provides detailed information about a scheduled query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.describe_scheduled_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#describe_scheduled_query)
        """

    def execute_scheduled_query(
        self,
        *,
        ScheduledQueryArn: str,
        InvocationTime: Union[datetime, str],
        ClientToken: str = ...
    ) -> None:
        """
        You can use this API to run a scheduled query manually.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.execute_scheduled_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#execute_scheduled_query)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#generate_presigned_url)
        """

    def list_scheduled_queries(
        self, *, MaxResults: int = ..., NextToken: str = ...
    ) -> ListScheduledQueriesResponseTypeDef:
        """
        Gets a list of all scheduled queries in the caller's Amazon account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.list_scheduled_queries)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#list_scheduled_queries)
        """

    def list_tags_for_resource(
        self, *, ResourceARN: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List all tags on a Timestream query resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#list_tags_for_resource)
        """

    def prepare_query(
        self, *, QueryString: str, ValidateOnly: bool = ...
    ) -> PrepareQueryResponseTypeDef:
        """
        A synchronous operation that allows you to submit a query with parameters to be
        stored by Timestream for later running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.prepare_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#prepare_query)
        """

    def query(
        self, *, QueryString: str, ClientToken: str = ..., NextToken: str = ..., MaxRows: int = ...
    ) -> QueryResponseTypeDef:
        """
        `Query` is a synchronous operation that enables you to run a query against your
        Amazon Timestream data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#query)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence["TagTypeDef"]) -> Dict[str, Any]:
        """
        Associate a set of tags with a Timestream resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes the association of tags from a Timestream query resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#untag_resource)
        """

    def update_scheduled_query(
        self, *, ScheduledQueryArn: str, State: ScheduledQueryStateType
    ) -> None:
        """
        Update a scheduled query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.update_scheduled_query)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#update_scheduled_query)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_scheduled_queries"]
    ) -> ListScheduledQueriesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["query"]) -> QueryPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/client/#get_paginator)
        """
