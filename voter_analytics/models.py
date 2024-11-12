from django.db import models

# Create your models here.


class Voter(models.Model):
    """
    represent the data for 1 registered voter in Newton, MA dataset
    Fields:Voter ID Number, Last Name, First Name, Residential Address - Street Number,
    Residential Address - Street Name, Residential Address - Apartment Number,
    Residential Address - Zip Code, Date of Birth, Date of Registration,
    Party Affiliation, Precinct Number, v20state, v21town, v21primary,
    v22general, v23town, voter_score
    """

    # Identification
    voter_id = models.TextField()
    last_name = models.TextField()
    first_name = models.TextField()

    # Residential address
    residential_addr_street_number = models.TextField()
    residential_addr_street_name = models.TextField()
    residential_addr_apartment_number = models.TextField(blank=True, null=True)
    residential_addr_zip_code = models.TextField()

    # Voter details
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.TextField()
    precinct_number = models.TextField()

    # Voting history
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    # Scoring
    voter_score = models.IntegerField()

    def __str__(self):
        """
        A string representation of this Voter object
        """
        return f"{self.first_name} {self.last_name} - Voter ID: {self.voter_id}"


def load_data():
    """
    Function to load data records from CSV file into Django model instances
    """

    # delete existing records to prevent duplicates:
    Voter.objects.all().delete()

    filename = "/Users/trucduong/Desktop/cs412-hw/newton_voters.csv"

    f = open(filename)
    f.readline()  # discard headers

    for line in f:
        line = f.readline().strip()
        fields = line.split(",")

        # print(fields)

        try:
            # create a new instance of Voter object with this record from the CSV
            voter = Voter(
                voter_id=fields[0].strip(),
                last_name=fields[1].strip(),
                first_name=fields[2].strip(),
                # Residential address
                residential_addr_street_number=fields[3].strip(),
                residential_addr_street_name=fields[4],
                residential_addr_apartment_number=fields[5] if fields[5] else None,
                residential_addr_zip_code=fields[6],
                # Voter details
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9].strip(),
                precinct_number=fields[10].strip(),
                # Convert boolean fields for voting history fields
                v20state=fields[11].strip().upper() == "TRUE",
                v21town=fields[12].strip().upper() == "TRUE",
                v21primary=fields[13].strip().upper() == "TRUE",
                v22general=fields[14].strip().upper() == "TRUE",
                v23town=fields[15].strip().upper() == "TRUE",
                # Scoring
                voter_score=int(fields[16]),
            )

            # save to db
            voter.save()
            print(f"Created Voter: {voter}")
        except:
            print(f"Skipped: {fields}")

    print(f"Done. Created {len(Voter.objects.all())} Voter objects.")
