#!/usr/bin/python
#
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example locates a user profile by ID number and adds a filter to it,
limiting the user profile's access to certain advertisers. To get user IDs,
run get_users.py. To get advertiser IDs, run get_advertisers.py.

A similar pattern can be applied to set filters limiting site, user role,
and/or campaign access for any user. To get the Filter Criteria Type ID, run
get_user_filter_types.py.

Tags: user.getUser, user.saveUser
"""

__author__ = 'api.jdilallo@gmail.com (Joseph DiLallo)'

import os
import sys
sys.path.insert(0, os.path.join('..', '..', '..', '..'))

# Import appropriate classes from the client library.
from adspygoogle import DfaClient


USER_ID = 'INSERT_USER_ID_HERE'
ADVERTISER_ID = 'INSERT_ADVERTISER_ID_HERE'


def main(client, user_id, advertiser_id):
  # Initialize appropriate service.
  user_service = client.GetUserService(
      'https://advertisersapitest.doubleclick.net', 'v1.20')

  # Retrieve the user who is to be modified.
  user = user_service.GetUser(user_id)[0]

  # Create and configure a user filter.
  advertiser_filter = {
      # The following field has been filled in to make a filter that allows a
      # user to access only the assigned objects.
      # This value was determined using get_user_filter_types.py.
      'userFilterCriteriaId': '2',
      # Because this filter used the criteria type "Assigned" it is necessary
      # to specify what advertisers this user has access to. This next step
      # would be skipped for the criteria types "All" and "None".

      # Create a list of object filters to represent each object the user has
      # access to. Since this is an advertiser filter, the list elements
      # represent an advertiser each. The size of the list will need to match
      # the total number of advertisers the user is assigned.
      'objectFilters': [{
          'id': advertiser_id
      }]
  }

  # Add the filter to the user.
  user['advertiserUserFilter'] = advertiser_filter

  # Save the changes made and display a success message.
  result = user_service.SaveUser(user)

  if result:
    print 'User with ID \'%s\' was modified.' % result[0]['id']
  else:
    print 'No user was modified.'


if __name__ == '__main__':
  # Initialize client object.
  client = DfaClient(path=os.path.join('..', '..', '..', '..'))
  main(client, USER_ID, ADVERTISER_ID)

