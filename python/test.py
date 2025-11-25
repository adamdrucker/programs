class Guest:
    def __init__(self, name, tenant, company, keys, vax) -> None:
        self.name = name
        self.tenant = tenant
        self.company = company
        self.keys = keys
        self.vax = vax

class Tenant:
    def __init__(self, name, key_set) -> None:
        self.name = name
        self.key_set = key_set

# objects

UMASS = Tenant("University of Massachusetts", [23, 24, 25, 26, 27])
HARVARD = Tenant("Harvard University", [28, 29, 30, 31, 32, 33, 34])
NEU = Tenant("Northeastern University", [35, 36, 37, 38, 39])
MIT = Tenant("Massachusetts Institute of Technology", [40, 41, 42, 43, 44, 45, 46, 47, 48, 49])
BU = Tenant("Boston University", [50, 51, 52, 53, 54, 55])


Drucker_Adam = Guest("Adam Drucker", [UMASS, NEU, MIT], "TechSquare",[],True)


# Create a guest
# this is very broken
def create_guest(name):

    full_name = str(input("Guest's full name: "))
    # need to make a way to select tenants then add to empty list below
    guest_tenant = []
    guest_company = str(input("Company guest works for (this can be blank): "))
    checked_out_keys = []
    guest_vax = bool(input("Has the guest provided proof of vaccination (0 for false, 1 for true)?: "))
    name = Guest(full_name, guest_tenant, guest_company, checked_out_keys, guest_vax)
    


# Check what keys have not been checked out by tentant name
def check_available_keys(tenant):

    print(tenant.key_set)




def get_guest_key_list(guest_name):

    # grab list of tenants from guest then query for their key list

    pass

