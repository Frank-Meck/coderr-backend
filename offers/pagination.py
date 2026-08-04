from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError


class OfferPagination(PageNumberPagination):

    page_size = 10

    page_size_query_param = "page_size"

    max_page_size = 100

    def get_page_size(self, request):
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