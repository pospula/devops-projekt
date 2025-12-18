targetScope = 'subscription'

param location string = 'westeurope'
param rgName string = 'DevOps_Projekt_RG'
param acrName string = 'devopsprojekt123test' 

resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: rgName
  location: location
}

module resourcesModule 'resources.bicep' = {
  name: 'ResourcesDeployment'
  scope: rg
  params: {
    location: location
    acrName: acrName
  }
}
