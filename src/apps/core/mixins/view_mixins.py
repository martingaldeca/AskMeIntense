from django.shortcuts import get_object_or_404


class MultipleFieldLookupMixin:
    lookup_fields = []
    lookup_url_kwargs = []
    random_result_from_list = False

    def get_object(self):
        if self.lookup_url_kwargs and len(self.lookup_fields) != len(
            self.lookup_url_kwargs
        ):
            raise ValueError("lookup_fields and lookup_url_kwargs must be same length.")

        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {}

        for lookup_field, lookup_url_kwarg in zip(
            self.lookup_fields, self.lookup_url_kwargs
        ):
            lookup = lookup_url_kwarg if lookup_url_kwarg else lookup_field

            assert lookup in self.kwargs, (
                f"Expected view {self.__class__.__name__} to be called with a URL keyword argument "
                f'named "{lookup}". Fix your URL conf, or set the `.lookup_field` '
                "attribute on the view correctly."
            )

            filter_kwargs[lookup_field] = self.kwargs[lookup]

        if self.random_result_from_list:
            obj = queryset.filter(**filter_kwargs).order_by("?").first()
        else:
            obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj
