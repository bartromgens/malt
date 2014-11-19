from base.views import BaseView

from whisky.models import Whisky
from whisky.models import Distillery
from whisky.models import Region

class WhiskiesView(BaseView):
    template_name = "whiskies/index.html"

    def add_extra_info(self, malts):
        for malt in malts:
            malt.alcoholPercentage_int = int(malt.alcoholPercentage)
            malt.age_int = int(malt.age)

    def get_all_whiskies(self):
        malts = Whisky.objects.order_by("distillery")

        self.add_extra_info(malts)
        return malts

    def get_context_data(self, **kwargs):
        context = super(WhiskiesView, self).get_context_data(**kwargs)
        malts = self.get_all_whiskies()
        context['whiskies_list'] = malts

        context['whiskiessection'] = True
        return context


class DistilleriesView(BaseView):
    template_name = "distilleries/index.html"

    def get_all_distilleries(self):
        distilleries = Distillery.objects.order_by("name")

        return distilleries

    def get_context_data(self, **kwargs):
        context = super(DistilleriesView, self).get_context_data(**kwargs)
        distilleries = self.get_all_distilleries()
        context['distilleries_list'] = distilleries

        context['distilleriessection'] = True
        return context


class RegionsView(BaseView):
    template_name = "regions/index.html"

    def get_all_regions(self):
        distilleries = Region.objects.order_by("name")

        return distilleries

    def get_context_data(self, **kwargs):
        context = super(RegionsView, self).get_context_data(**kwargs)
        regions = self.get_all_regions()
        context['region_list'] = regions

        context['regionssection'] = True
        return context
