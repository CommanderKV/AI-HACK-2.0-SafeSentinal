window.onbeforeunload = function(event) {
  event.preventDefault();
  event.returnValue = '';
  alert(event.target.toString());
  console.log(event);
  console.log(event.currentTarget.location.href);
  return false;
}
