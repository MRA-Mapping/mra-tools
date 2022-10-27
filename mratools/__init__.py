MRA_DEF_PARS={'idx_field':'Incident_UUID', 'date_field':'Incident_Date', 'team_field':'Team'}
OES_DEF_PARS={'idx_field':'Incident_UUID', 'date_field':'Date', 'team_field':'Team'}

def _get_feature_(featureset,idx,val):
    """Get feature(s) that match specific value index"""
    return [feature for feature in featureset.features if feature.as_dict['attributes'][idx] == val]

def _get_features_(featureset, idx, vals):
    """Get feature(s) that match a list of values for an index"""
    return[feature for feature in featureset.features if feature.as_dict['attributes'][idx] in vals ]

def _get_geom_(feature):
    pass


##featureset accessors 
__feature_geom = lambda f: f.geom
__feature_attrs = lambda f: f.as_dict['attributes']
__features = lambda fs: fs.features

def _get_attr_(feature,idx):
    """get value of an attribute for a feature"""
    return __feature_attrs(feature).get(idx) 

def _get_attrs_(featureset, idx):
    """Get values for an attribute in a featureset"""
    return[__feature_attrs(feature).get(idx) for feature in __features(featureset)]

def _get_unique_attrs_(featureset, idx):
    """Get all unique values of an attribute in a featureset"""
    return set(_get_attrs_(featureset,idx=idx))


_nulchk_attr = lambda x: '' in x or None in x
_dupchk_attr = lambda x: len(x) > len(set(x)) 

def _check(s,tests):
    for test in tests.values():
        yield test(s)
        

def check_incidents(s, idx_field="Incident_UUID",date_field='Incident_Date', team_field="Team", external_incident_tests = None, 
**kwargs):
    """Sanity Check a feature set and return a structured record

    s  - incidents (FeatureSet) to check
    
    0: duplicates T/F- True if there are Duplicates
    1: NULL UUIDs T/F - True if there are Null or empty Incident UUIDS
    """
    
    incident_tests = {"Null Test":_nulchk_attr,
                      "Duplicate Test": _dupchk_attr,
                     }
    if external_incident_tests:
        incident_tests.update(external_incident_tests)
        
    attrs = _get_attrs_(s,idx_field)
  
    return (_ for _ in _check(attrs,incident_tests))

    
def check_points(s, idx_field="Linked_Incident_UUID",date_field='Linked_Incident_Date', team_field="Linked_Team", **kwargs):
    """Sanity Check a feature set and return a structured record

    s  - points (FeatureSet) to check
        
    0: duplicates T/F- True if there are Duplicates
    1: NULL UUIDs T/F - True if there are Null or empty Incident UUIDS
    """
    points_tests = {"Null Test":_nulchk_attr,
                      "Duplicate Test": _dupchk_attr,
                     }
    attrs = _get_attrs_(s,idx_field)
  
    return (_ for _ in _check(attrs,points_tests))
    
def cmp_incidents(s1,s2, idx_fields=("Incident_UUID","Incident_UUID",),date_fields=('Incident_Date','Date',), team_fields=("Team","Team",)):
    """Compare FeatureSets of incidents and return a structured record
    
    s1,s2 incidents (FeatureSets) to compare
    idx_field = field for index, can be a list of two elements if s1,s2 index field different.
    date_field = field for index, can be a list of two elements if s1,s2 index field different.
    team_field = field for index, can be a list of two elements if s1,s2 index field different.
    
    returned record structure/tuple:
    idx: test/type - Comment
    
    0: len_check/bool - len(s1)==len(s2)
    1: intersect/int  - number of features in intersection of s1,s2 by idx_field
    2: date_match/int - number of features in intersection of s1,s2 where dates match
    3: team_match/int - number of features in intersection of s1,s2 where the team names match
    4: point_match/int - number of features for all 
    """
    
    len_check = len(s1)==len(s2)
    
    s1_idxs = _get_unique_attrs_(s1, idx_fields[0])
    s2_idxs = _get_unique_attrs_(s2, idx_fields[1])
    
    isect = s1_idxs.intersection(s2_idxs)
    len_isect = len(isect)
    
    s1_ftrs = _get_features_(s1,idx_fields[0], isect)
    s2_ftrs = _get_features_(s2,idx_fields[1], isect)
    
    date_match = 0
    team_match = 0
    point_match = 0
    for feature in s1_ftrs:
        s2_feature, = _get_feature_(s2,idx_fields[1], _get_attr_(feature,idx_fields[0]))
        #print(feature, s2_feature)
        if s2_feature:
            
            if _get_attr_(feature, date_fields[0]) == _get_attr_(s2_feature, date_fields[1]):
                date_match = date_match+1

            if _get_attr_(feature, team_fields[0]) == _get_attr_(s2_feature, team_fields[1]):
                team_match = team_match+1
                
    return len_check, len_isect, date_match, team_match, point_match

                
                
                
                
                
            
    
    
    