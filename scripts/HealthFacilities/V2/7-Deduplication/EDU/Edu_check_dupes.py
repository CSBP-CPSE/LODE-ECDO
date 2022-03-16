import pandas as pd
import numpy as np

# df = pd.read_csv("output/ODEF_DupePairs.csv")


# print("Perofrming first check on full address...")
# def check_1(address, distance, isced020, isced1, isced2, isced3, isced4):
#     """
#     If full address is highly similar, ISCED levels are the same,
#     and distance between pair is small, label as duplicate.
#     """

#     compare = [isced1, isced2, isced3, isced4]
#     isced = sum(compare)

#     if np.isnan(distance):

#         if address >= 0.9 and isced == 4:
#             return True
#         else:
#             return False

#     else:

#         if address >= 0.9 and isced == 4 and distance < 5:
#             return True
#         else:
#             return False

# df["Check_1"] = df.apply(lambda x: check_1(address = x.Addr_CS, 
#                           distance = x.Distance,
#                           isced020 = x.ISCED020_Match,
#                           isced1 = x.ISCED1_Match,
#                           isced2 = x.ISCED2_Match,
#                           isced3 = x.ISCED3_Match,
#                           isced4 = x['ISCED4+_Match']), axis=1)
# print("Done.")



# print("Performing second check on parsed address...")
# def check_2(str_name, str_num, distance, isced020, isced1, isced2, isced3, isced4):
#     """
#     If parsed address is highly similar, ISCED levels are the same,
#     and distance between pair is small, label as duplicate.
#     """

#     compare = [isced1, isced2, isced3, isced4]
#     isced = sum(compare)

#     if np.isnan(distance):

#         if str_name >= 0.9 and str_num == 1 and isced == 4:
#             return True
#         else:
#             return False

#     else:

#         if str_name >= 0.9 and str_num == 1 and isced == 4 and distance < 5 :
#             return True
#         else:
#             return False

# df["Check_2"] = df.apply(lambda x: check_2(
#                           str_name = x.StrName_CS,
#                           str_num = x.StrNum_Match, 
#                           distance = x.Distance,
#                           isced020 = x.ISCED020_Match,
#                           isced1 = x.ISCED1_Match,
#                           isced2 = x.ISCED2_Match,
#                           isced3 = x.ISCED3_Match,
#                           isced4 = x['ISCED4+_Match']), axis=1)
# print("Done.")

# df.to_csv("output/dupe_check.csv",index = False)
# df.loc[(df.Check_1 == True) | (df.Check_2 == True)].to_csv("output/dupe_TRUE.csv", index = False)


# read database file used in 7-Dedup.
final = pd.read_csv("input/ODEF_Validation_ForDedupe.csv")

# read dedupe file
df = pd.read_csv("output/dupe_check_annotated.csv")


# discern which duplicate to keep
def hierarchy(id1, id2, orig):
    """
    if row is a duplicate, keep the idx that is not ESDC
    
    id1 = first id in duplicate pair
    id2 = second "
    dupe = manual annotation if duplicated (TRUE/FALSE)
    orig = manual annotation of idx to keep
    """
    try:
        if pd.isnull(orig):
            return "NA"

        else:
            check_provider1 = final.loc[final.idx == id1].provider.item()
            check_provider2 = final.loc[final.idx == id2].provider.item()

            esdc = "Employment and Social Development Canada"
            print(id1, id2)

            if check_provider1 != esdc and check_provider2 != esdc:
    #             print("both esdc, keeping original suggestion.")
                return orig

            elif check_provider1 == esdc and check_provider2 != esdc:
    #             print("Keeping id2 -- {}".format(check_provider2))
                return id2

            elif check_provider1 != esdc and check_provider2 == esdc:
    #             print("Keeping id1 -- {}".format(check_provider1))
                return id1

            elif check_provider1 == esdc and check_provider2 == esdc:
    #             print("both esdc, keeping original suggestion.")
                return orig
    
    except ValueError:
        return "Item not found."

print("Keeping non-ESDC id's...")
df["hierarchy_keep"] = df.apply(lambda x: hierarchy(
                                        id1 = x.idx1,
                                        id2 = x.idx2,
                                        orig = x.idx_keep), axis = 1)

    
df.to_csv("output/dupe_check_annotated.csv", index = False)
df.loc[df.manual == True].to_csv("output/dupe_check_annotated_TRUE.csv", index = False)
print("Done.")