$(document).ready(function(){

    $('#dropdown').on('change',function(e){
         e.preventDefault();
        var parca_turu = $(this).val();
        console.log("Secilen: "+parca_turu); 
        $.ajax({
            url:"",
            method:'GET',
          // send selected data to the parca_kayit method which is in views.py
            data : {'parcaAdi' : $(this).val()}, // 'parcaAdi' will be used in request.GET.get('parcaAdi') which is in views.py, $(this).val() is selected item, 
            success:function(gelen_parca_turu){
                //console.log(gelen_parca_turu);
            }
        });
    });
});