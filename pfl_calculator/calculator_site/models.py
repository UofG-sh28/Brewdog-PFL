from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    """This model represents a user's business,
        stores information about the Business' location, size, details and contacts.

        Primary Key:
            id - Uses auto ID as primary_key

        Dependencies:
            user - Each Business 'belongs' to one user.

        Fields:
            company_name - Required
            business_address - Optional
            area_type - Optional, choice
            part_of_world - Optional, choice
            business_type - Optional, choice
            contact_number - Optional
            contact_email - Optional
            business_size - Optional, choice
        """
    # Choices,
    # Using shortened names to keep tables clean, use get_FIELDNAME_display() for verbose names
    # These choices are just taken from excel sheet, easily altered.
    AREA_TYPES = (
        ("C", "Inner City"),
        ("U", "Urban"),
        ("R", "Rural"),
    )
    PARTS_OF_WORLD = (
        ("UK", "UK"),
        ("EU","Europe"),
        ("NA","North America"),
        ("GL","Global"),
    )
    BUSINESS_TYPES = (
        ("BNFNA", "Bar (no food, no accomodation)"),
        ("BNA", "Bar (serving food, no accomodation)"),
        ("R", "Restaurant"),
        ("HNF", "Hotel (no food)"),
        ("H", "Hotel (serving Food)"),
    )
    BUSINESS_TURNOVERS = (
        ("S", "£100k-£500k"),
        ("M", "£500k-£10,000k"),
        ("L", "Over £10,000k"),
    )
    #FK
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #FIELDS
    company_name = models.CharField(max_length=50)
    business_address = models.CharField(max_length=150)
    area_type = models.CharField(max_length=1, choices=AREA_TYPES)
    part_of_world = models.CharField(max_length=2, choices=PARTS_OF_WORLD)
    business_type = models.CharField(max_length=5, choices=BUSINESS_TYPES)
    contact_number = models.CharField(max_length=15)
    contact_email = models.EmailField(max_length=150)
    business_size = models.CharField(max_length=1, choices=BUSINESS_TURNOVERS)

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Businesses"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
        super(Business, self).save(*args, **kwargs)

class ConversionFactor(models.Model):
    """This model represents a year's conversion factors,
        These are used when converting a business' usage into their carbon footprint.

        Primary Key:
            id - Uses auto ID

        Dependencies:
            N/A

        Fields:
            year - the year this represents, unique (one ConversionFactor per year)
            All of the calculator fields, all are required.
        """
    #OTHER FIELDS
    year = models.IntegerField(unique=True)
    #CALCULATOR FIELDS
    mains_gas = models.FloatField(default=0.0)
    fuel = models.FloatField(default=0.0)
    oil = models.FloatField(default=0.0)
    coal = models.FloatField(default=0.0)
    wood = models.FloatField(default=0.0)
    grid_electricity = models.FloatField(default=0.0)
    grid_electricity_LOWCARBON = models.FloatField(default=0.0)
    waste_food_landfill = models.FloatField(default=0.0)
    waste_food_compost = models.FloatField(default=0.0)
    waste_food_charity = models.FloatField(default=0.0)
    bottles_recycle = models.FloatField(default=0.0)
    aluminum_can_recycle = models.FloatField(default=0.0)
    general_waste_landfill = models.FloatField(default=0.0)
    general_waste_recycle = models.FloatField(default=0.0)
    special_waste = models.FloatField(default=0.0)
    goods_delivered_company_owned = models.FloatField(default=0.0)
    goods_delivered_contracted = models.FloatField(default=0.0)
    travel_company_business = models.FloatField(default=0.0)
    flights_domestic = models.FloatField(default=0.0)
    flights_international = models.FloatField(default=0.0)
    staff_commuting = models.FloatField(default=0.0)
    beef_lamb = models.FloatField(default=0.0)
    other_meat = models.FloatField(default=0.0)
    lobster_prawn = models.FloatField(default=0.0)
    fin_fish_seafood = models.FloatField(default=0.0)
    milk_yoghurt = models.FloatField(default=0.0)
    cheeses = models.FloatField(default=0.0)
    fruit_veg_local = models.FloatField(default=0.0)
    fruit_veg_other = models.FloatField(default=0.0)
    dried_food = models.FloatField(default=0.0)
    beer_kegs = models.FloatField(default=0.0)
    beer_cans = models.FloatField(default=0.0)
    beer_bottles = models.FloatField(default=0.0)
    beer_kegs_LOWCARBON = models.FloatField(default=0.0)
    beer_cans_LOWCARBON = models.FloatField(default=0.0)
    beer_bottles_LOWCARBON = models.FloatField(default=0.0)
    soft_drinks = models.FloatField(default=0.0)
    wine = models.FloatField(default=0.0)
    spirits = models.FloatField(default=0.0)
    kitchen_equipment_asssets = models.FloatField(default=0.0)
    building_repair_maintenance = models.FloatField(default=0.0)
    cleaning = models.FloatField(default=0.0)
    IT_Marketing = models.FloatField(default=0.0)
    main_water = models.FloatField(default=0.0)
    sewage = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Convertion Factor"
        verbose_name_plural = "Convertion Factors"

    def save(self, *args, **kwargs):
        super(ConversionFactor, self).save(*args, **kwargs)

class BusinessUsage(models.Model):
    """ This model stores the usage numbers of one year of a business (inputs to the calculator).
        Also stores the conversion factor ID for the corresponding year.

        Primary Key:
            id - Uses Auto Generated ID

        Dependencies:
            business - This usage belongs to exactly one business
            conversion_factor - This usage must have a related ConversionFactor

        Field:
            business - FK
            conversion_factor _ FK
            All the calculator fields with help text to indicate which unit is specified."""
    #OTHER FIELDS
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    conversion_factor = models.ForeignKey(ConversionFactor, on_delete=models.RESTRICT)
    year = models.IntegerField()
    #CALCULATOR FIELDS
    mains_gas = models.IntegerField()
    fuel = models.IntegerField()
    oil = models.IntegerField()
    coal = models.IntegerField()
    wood = models.IntegerField()
    grid_electricity = models.IntegerField()
    grid_electricity_LOWCARBON = models.IntegerField()
    waste_food_landfill = models.IntegerField()
    waste_food_compost = models.IntegerField()
    waste_food_charity = models.IntegerField()
    bottles_recycle = models.IntegerField()
    aluminum_can_recycle = models.IntegerField()
    general_waste_landfill = models.IntegerField()
    general_waste_recycle = models.IntegerField()
    special_waste = models.IntegerField()
    goods_delivered_company_owned = models.IntegerField()
    goods_delivered_contracted = models.IntegerField()
    travel_company_business = models.IntegerField()
    flights_domestic = models.IntegerField()
    flights_international = models.IntegerField()
    staff_commuting = models.IntegerField()
    beef_lamb = models.IntegerField()
    other_meat = models.IntegerField()
    lobster_prawn = models.IntegerField()
    fin_fish_seafood = models.IntegerField()
    milk_yoghurt = models.IntegerField()
    cheeses = models.IntegerField()
    fruit_veg_local = models.IntegerField()
    fruit_veg_other = models.IntegerField()
    dried_food = models.IntegerField()
    beer_kegs = models.IntegerField()
    beer_cans = models.IntegerField()
    beer_bottles = models.IntegerField()
    beer_kegs_LOWCARBON = models.IntegerField()
    beer_cans_LOWCARBON = models.IntegerField()
    beer_bottles_LOWCARBON = models.IntegerField()
    soft_drinks = models.IntegerField()
    wine = models.IntegerField()
    spirits = models.IntegerField()
    kitchen_equipment_asssets = models.DecimalField(max_digits=16, decimal_places=2)
    building_repair_maintenance = models.DecimalField(max_digits=16, decimal_places=2)
    cleaning = models.DecimalField(max_digits=16, decimal_places=2)
    IT_Marketing = models.DecimalField(max_digits=16, decimal_places=2)
    main_water = models.IntegerField()
    sewage = models.DecimalField(max_digits=16, decimal_places=2)

    class Meta:
        verbose_name = "Business Usage"
        verbose_name_plural = "Business Usages"

    def save(self, *args, **kwargs):
        super(BusinessUsage, self).save(*args, **kwargs)

class BusinessMetrics(models.Model):
    """ This stores a business' yearly metrics BusinessMetrics.

    Primary Key:
        id - uses auto id

    Dependencies:
        business - each business has metrics for each year.

    Fields:
        year - Optional
        operating_months - Optional
        weekly_openings - Optional
        annual_meals - Optional
        annual_drinks - Optional
        annual_customers - Optional
        revenue - Optional."""

    #FK
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    #FIELDS
    year = models.IntegerField()
    operating_months = models.IntegerField()
    weekly_openings = models.IntegerField()
    annual_meals = models.IntegerField()
    annual_drinks = models.IntegerField()
    annual_customers = models.IntegerField()
    revenue = models.IntegerField()

    class Meta:
        verbose_name = "Business Metric"
        verbose_name_plural = "Business Metrics"

    def save(self, *args, **kwargs):
        super(BusinessMetrics, self).save(*args, **kwargs)

class CarbonFootprint(models.Model):
    """This stores a User's carbon footprint which is a combination of a year's Usage & ConversionFactor.

    Primary Key:
        id - uses auto id

    Dependencies:
        user
        business
        business_usage
        conversion_factor

    Fields:
        business - Required, FK
        year - Required
        json - json representation of the carbon footprint.
        All the calculator fields, storing the amount of carbon generated by each field."""



    # ForeignKey
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    #OTHER FIELDS
    year = models.IntegerField()
    #CALCULATOR FIELDS
    mains_gas = models.FloatField(default=0.0)
    fuel = models.FloatField(default=0.0)
    oil = models.FloatField(default=0.0)
    coal = models.FloatField(default=0.0)
    wood = models.FloatField(default=0.0)
    grid_electricity = models.FloatField(default=0.0)
    grid_electricity_LOWCARBON = models.FloatField(default=0.0)
    waste_food_landfill = models.FloatField(default=0.0)
    waste_food_compost = models.FloatField(default=0.0)
    waste_food_charity = models.FloatField(default=0.0)
    bottles_recycle = models.FloatField(default=0.0)
    aluminum_can_recycle = models.FloatField(default=0.0)
    general_waste_landfill = models.FloatField(default=0.0)
    general_waste_recycle = models.FloatField(default=0.0)
    special_waste = models.FloatField(default=0.0)
    goods_delivered_company_owned = models.FloatField(default=0.0)
    goods_delivered_contracted = models.FloatField(default=0.0)
    travel_company_business = models.FloatField(default=0.0)
    flights_domestic = models.FloatField(default=0.0)
    flights_international = models.FloatField(default=0.0)
    staff_commuting = models.FloatField(default=0.0)
    beef_lamb = models.FloatField(default=0.0)
    other_meat = models.FloatField(default=0.0)
    lobster_prawn = models.FloatField(default=0.0)
    fin_fish_seafood = models.FloatField(default=0.0)
    milk_yoghurt = models.FloatField(default=0.0)
    cheeses = models.FloatField(default=0.0)
    fruit_veg_local = models.FloatField(default=0.0)
    fruit_veg_other = models.FloatField(default=0.0)
    dried_food = models.FloatField(default=0.0)
    beer_kegs = models.FloatField(default=0.0)
    beer_cans = models.FloatField(default=0.0)
    beer_bottles = models.FloatField(default=0.0)
    beer_kegs_LOWCARBON = models.FloatField(default=0.0)
    beer_cans_LOWCARBON = models.FloatField(default=0.0)
    beer_bottles_LOWCARBON = models.FloatField(default=0.0)
    soft_drinks = models.FloatField(default=0.0)
    wine = models.FloatField(default=0.0)
    spirits = models.FloatField(default=0.0)
    kitchen_equipment_asssets = models.FloatField(default=0.0)
    building_repair_maintenance = models.FloatField(default=0.0)
    cleaning = models.FloatField(default=0.0)
    IT_Marketing = models.FloatField(default=0.0)
    main_water = models.FloatField(default=0.0)
    sewage = models.FloatField(default=0.0)

    class Meta:
        verbose_name = "Carbon Footprint"
        verbose_name_plural = "Carbon Footprints"

    def __str__(self):
        try:
            verbose = f"{self.business.company_name}'s Carbon Footprint for {self.year}"
            return verbose
        except:
            return "Carbon Footprint"

    def save(self, *args, **kwargs):
        super(CarbonFootprint, self).save(*args, **kwargs)
