
function decorateResult(result) {
  if(result.loading){
    return "Searching..."
  }
  if(result.parent_title == null){
    return "";
  }
  var $ret = $('<div class="res_section"><span>' + result.parent_title + '</span><div class="res_subsection">' + result.title + '</div><div class="res_text">' + result.relevant_text + '</div>');
  return $ret;
};


function initSearch(version){

    $(document).ready(function() {

        $('#search').select2({
          placeholder: "Search Conan Docs",
          allowClear: true,
          templateResult: decorateResult,
          minimumInputLength: 2,
          ajax: {
            delay: 350,
            method: "GET",
            dataType: 'json',
            url: 'https://3ghmj80y32.execute-api.us-east-1.amazonaws.com/api/search',
            //url: 'http://127.0.0.1:8000/search',
            data: function (params) {
                      if(!params.term){
                        return -1;
                      }
                      var query = {
                        query: params.term,
                        version: version
                       }
                       return query;
                  },
            async: false,
            crossDomain: true,
            contentType: 'application/json',
            processResults: function (data) {
              // Transforms the top-level key of the response object from 'items' to 'results'
              console.log(data["time"]);
              var elements = []
              data.results.forEach(function(el) {
                 el.id = el.slug;
                 el.text = el.title;
                 if(!el.parent_title){
                    el.parent_title = el.text;
                 }
                 if(!el.relevant_text){
                    el.relevant_text = el.title;
                 }
                 elements.push(el);
              });
              return {
                results: elements
              };
            }
          }
        });
    });
 }
