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

class Channeldecline(BaseObject):
	"""
	
	"""

	__config = {
		
		"9ffc84e8-a5bc-4faf-b24a-33f9fa63366e" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/declines/channels", "delete", [], []),
		
		"9018ae49-6d75-49de-b343-817003c0b44a" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/declines/channels", "query", [], []),
		
		"b4139e3f-42c9-4bb2-af63-8ad31056ba6c" : OperationConfig("/issuer/spendcontrols/v1/card/{uuid}/controls/declines/channels", "create", [], []),
		
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
		Delete object of type Channeldecline by id

		@param str id
		@return Channeldecline of the response of the deleted instance.
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

		return BaseObject.execute("9ffc84e8-a5bc-4faf-b24a-33f9fa63366e", Channeldecline(mapObj))

	def delete(self):
		"""
		Delete object of type Channeldecline

		@return Channeldecline of the response of the deleted instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("9ffc84e8-a5bc-4faf-b24a-33f9fa63366e", self)








	@classmethod
	def query(cls,criteria):
		"""
		Query objects of type Channeldecline by id and optional criteria
		@param type criteria
		@return Channeldecline object representing the response.
		@raise ApiException: raised an exception from the response status
		"""

		return BaseObject.execute("9018ae49-6d75-49de-b343-817003c0b44a", Channeldecline(criteria))

	@classmethod
	def create(cls,mapObj):
		"""
		Creates object of type Channeldecline

		@param Dict mapObj, containing the required parameters to create a new object
		@return Channeldecline of the response of created instance.
		@raise ApiException: raised an exception from the response status
		"""
		return BaseObject.execute("b4139e3f-42c9-4bb2-af63-8ad31056ba6c", Channeldecline(mapObj))







