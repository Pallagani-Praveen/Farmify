$(document).ready(()=>{
    $("#pincode").on('input',function(){
        let pin = $(this).val();
        let url = 'http://www.postalpincode.in/api/pincode/'+pin;
        $.get(url, function(data, status){
            if(data.Status==='Success'){
                var villages = data.PostOffice;
                villages.forEach(village => {
                    addNewOption(village.Name);
                });
            }
            else{
                resetOption('--None--');
            }
          });
    });
});

function resetOption(name){
    var select = document.getElementById('area');
    let option = document.createElement('option');
    option.value = name;
    option.text = name;
    if(select.childElementCount!=1){
        while(select.firstChild){
            select.removeChild(select.firstChild);
        }
        select.appendChild(option);
    }
}

function addNewOption(name){
    var select = document.getElementById('area');
    let option = document.createElement('option');
    option.value = name;
    option.text = name;
    select.appendChild(option);
    
}

