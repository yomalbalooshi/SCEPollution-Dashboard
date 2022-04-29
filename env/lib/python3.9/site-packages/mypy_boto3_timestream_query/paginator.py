"""
Type annotations for timestream-query service client paginators.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_timestream_query.client import TimestreamQueryClient
    from mypy_boto3_timestream_query.paginator import (
        ListScheduledQueriesPaginator,
        ListTagsForResourcePaginator,
        QueryPaginator,
    )

    session = Session()
    client: TimestreamQueryClient = session.client("timestream-query")

    list_scheduled_queries_paginator: ListScheduledQueriesPaginator = client.get_paginator("list_scheduled_queries")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    query_paginator: QueryPaginator = client.get_paginator("query")
    ```
"""
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator
from botocore.paginate import Paginator as Boto3Paginator

from .type_defs import (
    ListScheduledQueriesResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    PaginatorConfigTypeDef,
    QueryResponseTypeDef,
)

__all__ = ("ListScheduledQueriesPaginator", "ListTagsForResourcePaginator", "QueryPaginator")


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListScheduledQueriesPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.ListScheduledQueries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#listscheduledqueriespaginator)
    """

    def paginate(
        self, *, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListScheduledQueriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.ListScheduledQueries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#listscheduledqueriespaginator)
        """


class ListTagsForResourcePaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.ListTagsForResource)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#listtagsforresourcepaginator)
    """

    def paginate(
        self, *, ResourceARN: str, PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#listtagsforresourcepaginator)
        """


class QueryPaginator(Boto3Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.Query)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#querypaginator)
    """

    def paginate(
        self,
        *,
        QueryString: str,
        ClientToken: str = ...,
        PaginationConfig: "PaginatorConfigTypeDef" = ...
    ) -> _PageIterator[QueryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/timestream-query.html#TimestreamQuery.Paginator.Query.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_timestream_query/paginators/#querypaginator)
        """
