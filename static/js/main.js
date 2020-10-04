document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems, {});
});

const bagSelector  = document.getElementById('bag-selector'); // number of bags selector
bagSelector.addEventListener('click', event => { // when a number of bags is selected in the radio buttons
    const isInput = event.target.nodeName === 'INPUT';

    if (!isInput){  
        // if its clicked inside the bag-selector container, but is not input, do nothing
        return
    }
              
    const nrBags = event.target.id.split('-')[1] // number of bags
    
    const tripsDisplay  = document.getElementById('trips-display'); // container of all the trips 
    const allTripsDisplay = tripsDisplay.getElementsByClassName('tripsPerBag'); // all containers of each bag-trips set  
    const allTripsDisplayArr = Array.from(allTripsDisplay) // same as before, but in array, so it can be easy to loop through
    
    allTripsDisplayArr.forEach(function(tripBag){ // loop through array of containers of each bag-trip set
        if (tripBag.id === `trips-${nrBags}`){ // is this bag display container the one corresponding to the selected radio button
                if (tripBag.style.display === "none"){ // if is not showing, show
                    tripBag.style.display = "block";
                    document.getElementById('select-bags-alert').style.display = 'none'; // hide alert
                }
        }
        else{
            tripBag.style.display = 'none' // hide all the other trip-bag containers that were not selected
        }
    })
})
