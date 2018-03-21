function statusChangeCallback(response) {
	console.log(response);
	
	/* The response object is returned with a status field that lets the
     app know the current login status of the person.
     */
	if (response.status === 'connected') {
		testAPI();
	} else {
		  /* The person is not logged into your app or we are unable to tell.
			document.getElementById('status').innerHTML = 'Please log ' +
			'into this app.';*/
		
	}
}

function checkLoginState() {
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});
}

//This function automatically invokes when our website page is invoked.
//appId is uniqueID for the facebookDevelopers who want to use the facebook button in their websites.
window.fbAsyncInit = function() {
	FB.init({
		appId : '566912420329934',
		cookie : true,
		xfbml : true,
		version : 'v2.8'
	});
	FB.getLoginStatus(function(response) {
		statusChangeCallback(response);
	});

};

(function(d, s, id) {
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id))
		return;
	js = d.createElement(s);
	js.id = id;
	js.src = "https://connect.facebook.net/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

//TestApi() is used to welcome our customer using the facebook login
function testAPI() {
	console.log('Welcome!  Fetching your information.... ');
	FB.api('/me', function(response) {
		console.log('Successful login for: ' + response.name);
		document.getElementById('status').innerHTML = 'Thanks for logging in, '
				+ response.name + '!';
	});
}

//Google SignIN function
function onSignIn(googleUser) {
	var profile = googleUser.getBasicProfile();

	$(".g-signin2").hide();
	$(".container").hide();
	$("#login").hide();
	$("#hh3").hide();
	$("#gmail").show();
	$("#email111").text(profile.getEmail());

	console.log('ID: ' + profile.getId());
	console.log('Name: ' + profile.getName());
	console.log('Image URL: ' + profile.getImageUrl());
	console.log('Email: ' + profile.getEmail());
}

//Google SingnOut function
function signOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function() {
		alert("You have been successfully signed out");
		$("#login").show();
		$("#hh3").show();
		$(".g-signin2").show();
		$(".container").show();
		$("#gmail").hide();
	});
}

/* Still we have to workout on the linkedln part */

//when user clicks the linkedin Button 
function onLinkedInLoad() {
	IN.Event.on(IN, "auth", getProfileData);
}

// Use the API call wrapper to request the member's profile data
function getProfileData() {
	IN.API.Profile("me").fields("id", "first-name", "last-name", "headline",
			"location", "picture-url", "public-profile-url", "email-address")
			.result(displayProfileData).error(onError);
}

// Handle the successful return from the API call
function displayProfileData(data) {
	var user = data.values[0];
	document.getElementById("picture").innerHTML = '<img src="'
			+ user.pictureUrl + '" />';
	document.getElementById("name").innerHTML = user.firstName + ' '
			+ user.lastName;
	document.getElementById("intro").innerHTML = user.headline;
	document.getElementById("email").innerHTML = user.emailAddress;
	document.getElementById("location").innerHTML = user.location.name;
	document.getElementById("link").innerHTML = '<a href="'
			+ user.publicProfileUrl + '" target="_blank">Visit profile</a>';
	document.getElementById('profileData').style.display = 'block';
}

function onError(error) {
	console.log(error);
}

function logout() {
	IN.User.logout(removeProfileData);
}

function removeProfileData() {
	document.getElementById('profileData').remove();
}