function Register()
{
   //First you need to do some validation
   var username = document.getElementById("usernameInputField").value;
   var email = document.getElementById("emailInputField").value;
   //Password, Gender, etc...
   //Then start doing your validation the way you like it...
   /*if(password.length<6)
     {
         alert("Password is too short");
         return false;
     }
   */
   //Then when everything is valid, Post to the Server
   //This is a PHP Post Call
   $.post("Register.php",{ username:username,email:email } ,function(data) {
       //more codes
   });
}