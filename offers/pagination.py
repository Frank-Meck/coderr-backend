"""
Pagination configuration for the offers API.

Defines the default and maximum page sizes and allows clients
to customize the number of offers returned per page.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


class OfferPagination(PageNumberPagination):
    """
    Configure pagination for the offers API.

    The default page size is 10 items, while clients can provide
    a custom page size using the `page_size` query parameter.
    The maximum allowed page size is limited to 100 items.
    """

    page_size = 10

    page_size_query_param = "page_size"

    max_page_size = 100

    def get_page_size(self, request):
        """
        Return the requested page size.

        Validates the `page_size` query parameter and limits it
        to the configured maximum page size. If no page size is
        provided, the default page size is returned.
        """

        page_size = request.query_params.get(
            self.page_size_query_param
        )

        if page_size:
            try:
                page_size = int(page_size)

            except ValueError:
                raise ValidationError(
                    {
                        "page_size": "A valid integer is required."
                    }
                )

            if page_size > self.max_page_size:
                page_size = self.max_page_size

            return page_size

        return self.page_size
