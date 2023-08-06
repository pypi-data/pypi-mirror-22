#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#


from mastercardapicore import BaseObject
from mastercardapicore import RequestMap
from mastercardapicore import OperationConfig
from mastercardapicore import OperationMetadata
from resourceconfig import ResourceConfig

class Alertall(BaseObject):
	"""
	
	"""

	__config = {
		
		"c7f45a37-7615-4276-ac85-68f725a0ceb4" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/alerts/all", "delete", [], []),
		
		"bc71c5ea-f503-4a37-bcbb-0f1cedd3ba9e" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/alerts/all", "query", [], []),
		
		"9ef5dcb7-c931-467c-8895-6bd5f4c370a8" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/alerts/all", "create", [], []),
		
	}

	def getOperationConfig(self,operationUUID):
		if operationUUID not in self.__config:
			raise Exception("Invalid operationUUID: "+operationUUI)

		return self.__config[operationUUID]

	def getOperationMetadata(self):
		return OperationMetadata(ResourceConfig.getInstance().getVersion(), ResourceConfig.getInstance().getHost(), ResourceConfig.getInstance().getContext())





	@classmethod
	def deleteById(cls,id,map=None):
		"""
		Delete object of type Alertall by id

		@param str id
		@return Alertall of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""

		mapObj =  RequestMap()
		if id:
			mapObj.set("id", id)

		if map:
			if (isinstance(map,RequestMap)):
				mapObj.setAll(map.getObject())
			else:
				mapObj.setAll(map)

		return BaseObject.execute("c7f45a37-7615-4276-ac85-68f725a0ceb4", Alertall(mapObj))

	def delete(self):
		"""
		Delete object of type Alertall

		@return Alertall of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("c7f45a37-7615-4276-ac85-68f725a0ceb4", self)








	@classmethod
	def query(cls,criteria):
		"""
		Query objects of type Alertall by id and optional criteria
		@param type criteria
		@return Alertall object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("bc71c5ea-f503-4a37-bcbb-0f1cedd3ba9e", Alertall(criteria))

	@classmethod
	def create(cls,mapObj):
		"""
		Creates object of type Alertall

		@param Dict mapObj, containing the required parameters to create a new object
		@return Alertall of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("9ef5dcb7-c931-467c-8895-6bd5f4c370a8", Alertall(mapObj))







