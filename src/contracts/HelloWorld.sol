pragma solidity ^0.4.22;

contract HelloWorld {
    string public message;

    constructor() public {
        message = "Hello, World!";
        
    }
    
    function setMessage(string text) public payable{
        require(msg.value >= 0.01 ether);
        message = text;
    }

}