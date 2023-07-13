import requests
import json  # importing libs


class GetBranchesAndSort():
    """This class allow user to interact with REST API. 
    It takes two arguments as <branch1> and <branch2>
    then it make request to https://rdb.altlinux.org/api/
    that return lists due to arguments taken before 
    then it compare these two lists and return
    vocabulary that contain packages:
    that are in branch1 but not in branch2;
    that are in branch2 but not in branch1;
    packages where version-relise more in sysyphus then in p10"""

    
    def __init__(self, branch1, branch2) -> json:
        """code that allow use varaibles like self.varaible in class methods"""
        self.b1 = branch1
        self.b2 = branch2

    
    def main(self):
        """this is main method that allow to run all methods that are included in class"""
        
        GetBranchesAndSort.getPackages(self)
        result = json.dumps(GetBranchesAndSort.sort(self), indent=4)
        with open("result.json", "w") as f:
            f.write(result)
        

    
    def getPackages(self):
        """this method get packages from REST API URL's and convert it into json"""
        
        if requests.get("https://rdb.altlinux.org/api/export/branch_binary_packages/" + self.b1).status_code == 200:
            self.b1 = requests.get("https://rdb.altlinux.org/api/export/branch_binary_packages/" + self.b1).json()["packages"]
        else: print("REST API is unavailable")   
        
        if requests.get("https://rdb.altlinux.org/api/export/branch_binary_packages/" + self.b2).status_code == 200:
            self.b2 = requests.get("https://rdb.altlinux.org/api/export/branch_binary_packages/" + self.b2).json()["packages"]
        else: print("REST API is unavailable")
    
    
    def sort(self):
        """this method parsing packages than sort them due to technical specification"""
        
        packagesInP10NotInSisyp = []
        packagesInSisypNotInP10 = []
        packagesVersionDiffers = []


        ### comparing ###
        for element in self.b1:
            if element not in self.b2:
                packagesInP10NotInSisyp.append(element)
        
        print("first list done")
        
        for element in self.b2:
            if element not in self.b1:
                packagesInSisypNotInP10.append(element)

        print("second list done")

        for element in self.b1:
            for element2 in self.b2:
                if float(element2["version"]) > float(element["version"]):
                    packagesVersionDiffers.append(element2)
        print("last list done")
        ### comparing ###
        ### creating json structure ###
        result = {
            "packagesInP10NotInSisyp":  packagesInP10NotInSisyp,
            "packagesInSisypNotInP10": packagesInSisypNotInP10,
            "packagesVersionDiffers": packagesVersionDiffers
        }
        ### creating json structure ###
        return result



if __name__ == "__main__":
    obj = GetBranchesAndSort("p10", "sisyphus")
    obj.main()