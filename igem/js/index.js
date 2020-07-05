var ids=['HQ_page','content','bodyContent','mw-content-text']
for(var i=0;i<ids.length;i++)
document.querySelector('#'+ids[i]).removeAttribute('id');var classes=['mw-content-ltr']
for(var i=0;i<classes.length;i++)
{var elements=document.querySelectorAll('.'+classes[i]);for(var j=0;j<elements.length;j++)
{elements[j].classList.remove(classes[i]);}}
alert('JS works!');