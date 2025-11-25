function copyFunc() {
	
	var copyText = document.getElementByID("link");
	
	copyText.select();
	
	document.execCommand("copy");
	
}
