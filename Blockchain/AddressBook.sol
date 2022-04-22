//Address Book Contract can be used to store multiple smart contracts at the Blockchain and finde them later on
pragma solidity ^0.8.7;

contract AddressBook {
    
    address[] private _addresses;
    
    function getAddresses() public view  returns (address [] memory) {
        return _addresses;
    }
    function addAddress(address addr) public payable {
        _addresses.push(addr);
    }   
    
    function removeAddress(address addr) public payable{
        int256 value = getArrayIndex(addr);
        if(value != -1){
        uint256 index = uint256(value);
        for (uint i = index; i < _addresses.length-1; i++){
            _addresses[i] = _addresses[i+1];
        }
        delete _addresses[_addresses.length-1];
        
        }
    }
    
    function getArrayIndex(address addr) private view returns(int256){
        int256  j = 0;
        for(uint256 i = 0; i < _addresses.length; i++){
            if(_addresses[i] == addr){
                return  j;
            }
            j++;
        }
        return -1;
    }    
}