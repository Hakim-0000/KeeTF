
         

<!DOCTYPE html>
<html lang="en" >
<head>
   <title>Authentication - GLPI</title>

   <meta charset="utf-8" />

      <meta http-equiv="X-UA-Compatible" content="IE=edge" />

      <meta name="viewport" content="width=device-width, initial-scale=1" />

   <meta property="glpi:csrf_token" content="6fb9ef6d74bf0a4dd847f011e6d42aab86bfe92fd33f2ffd64a4b86dda2340b0" />

         <link rel="stylesheet" type="text/css" href="/glpi/public/lib/base.min.css?v=36c4962a6e7f933b22bc99d065c14be8272b4cdf" />
         <link rel="stylesheet" type="text/css" href="/glpi/css_compiled/css_palettes_auror.min.css?v=36c4962a6e7f933b22bc99d065c14be8272b4cdf" />
   
   

   <link rel="shortcut icon" type="images/x-icon" href="/glpi/pics/favicon.ico" />

         <script type="text/javascript" src="/glpi/public/lib/base.min.js?v=36c4962a6e7f933b22bc99d065c14be8272b4cdf"></script>
         <script type="text/javascript" src="/glpi/js/common.min.js?v=36c4962a6e7f933b22bc99d065c14be8272b4cdf"></script>
   
   
   <script type="text/javascript">
//<![CDATA[

         $(function() {
            i18n.setLocale('en_US');
         });            $(function() {
               $.ajax({
                  type: 'GET',
                  url: '/glpi/front/locale.php?domain=glpi&v=36c4962a6e7f933b22bc99d065c14be8272b4cdf',
                  success: function(json) {
                     i18n.loadJSON(json, 'glpi');
                  }
               });
            });

//]]>
</script>
</head>

<body class="welcome-anonymous">
   <div class="page-anonymous">
      <div class="flex-fill d-flex flex-column justify-content-center py-4 mt-4">
                                                
         <div class="container-tight py-6" style="max-width: 60rem">
            <div class="text-center">
               <div class="col-md">
                  <span class="glpi-logo mb-4" title="GLPI"></span>
               </div>
            </div>
            <div class="card card-md">
               <div class="card-body">
                  <form action="/glpi/front/login.php" method="post" autocomplete="off"  data-submit-once>
      <input type="hidden" name="noAUTO" value="0" />
      <input type="hidden" name="redirect" value="" />
      <input type="hidden" name="_glpi_csrf_token" value="d2afd80f8e6b996189e57ac9e42b066c39ba888eed6238dc9e66e1a14b825737" />

      <div class="row justify-content-center">
         <div class="col-md-5">

            <h2 class="card-header text-center mb-4">Login to your account</h2>
            <div class="mb-3">
               <label class="form-label">Login</label>
               <input type="text" class="form-control" id="login_name" name="fielda65d35234b8b5a" placeholder="" tabindex="1" />
            </div>
            <div class="mb-4">
               <label class="form-label">
                  Password

                                 </label>
               <input type="password" class="form-control" name="fieldb65d35234b8b5e" placeholder="" autocomplete="off" tabindex="2" />
            </div>

            
                           <div class="mb-3">
                  <label class="form-label">Login source</label>
                  <select name='auth' id='dropdown_auth1' class="form-select" size='1'><option value='local' selected>GLPI internal database</option></select><script type="text/javascript">
//<![CDATA[

$(function() {
         const select2_el = $('#dropdown_auth1').select2({
            
            width: '100%',
            dropdownAutoWidth: true,
            dropdownParent: $('#dropdown_auth1').closest('div.modal, body'),
            quietMillis: 100,
            minimumResultsForSearch: 10,
            matcher: function(params, data) {
               // store last search in the global var
               query = params;

               // If there are no search terms, return all of the data
               if ($.trim(params.term) === '') {
                  return data;
               }

               var searched_term = getTextWithoutDiacriticalMarks(params.term);
               var data_text = typeof(data.text) === 'string'
                  ? getTextWithoutDiacriticalMarks(data.text)
                  : '';
               var select2_fuzzy_opts = {
                  pre: '<span class="select2-rendered__match">',
                  post: '</span>',
               };

               if (data_text.indexOf('>') !== -1 || data_text.indexOf('<') !== -1) {
                  // escape text, if it contains chevrons (can already be escaped prior to this point :/)
                  data_text = jQuery.fn.select2.defaults.defaults.escapeMarkup(data_text);
               }

               // Skip if there is no 'children' property
               if (typeof data.children === 'undefined') {
                  var match  = fuzzy.match(searched_term, data_text, select2_fuzzy_opts);
                  if (match == null) {
                     return false;
                  }
                  data.rendered_text = match.rendered_text;
                  data.score = match.score;
                  return data;
               }

               // `data.children` contains the actual options that we are matching against
               // also check in `data.text` (optgroup title)
               var filteredChildren = [];

               $.each(data.children, function (idx, child) {
                  var child_text = typeof(child.text) === 'string'
                     ? getTextWithoutDiacriticalMarks(child.text)
                     : '';

                  if (child_text.indexOf('>') !== -1 || child_text.indexOf('<') !== -1) {
                     // escape text, if it contains chevrons (can already be escaped prior to this point :/)
                     child_text = jQuery.fn.select2.defaults.defaults.escapeMarkup(child_text);
                  }

                  var match_child = fuzzy.match(searched_term, child_text, select2_fuzzy_opts);
                  var match_text  = fuzzy.match(searched_term, data_text, select2_fuzzy_opts);
                  if (match_child !== null || match_text !== null) {
                     if (match_text !== null) {
                        data.score         = match_text.score;
                        data.rendered_text = match_text.rendered;
                     }

                     if (match_child !== null) {
                        child.score         = match_child.score;
                        child.rendered_text = match_child.rendered;
                     }
                     filteredChildren.push(child);
                  }
               });

               // If we matched any of the group's children, then set the matched children on the group
               // and return the group object
               if (filteredChildren.length) {
                  var modifiedData = $.extend({}, data, true);
                  modifiedData.children = filteredChildren;

                  // You can return modified objects from here
                  // This includes matching the `children` how you want in nested data sets
                  return modifiedData;
               }

               // Return `null` if the term should not be displayed
               return null;
            },
            templateResult: templateResult,
            templateSelection: templateSelection,
         })
         .bind('setValue', function(e, value) {
            $('#dropdown_auth1').val(value).trigger('change');
         })
         $('label[for=dropdown_auth1]').on('click', function(){ $('#dropdown_auth1').select2('open'); });
         $('#dropdown_auth1').on('select2:open', function(e){
            const search_input = document.querySelector(`.select2-search__field[aria-controls='select2-${e.target.id}-results']`);
            if (search_input) {
               search_input.focus();
            }
         });
      });

//]]>
</script>
               </div>
            
                           <div class="mb-2">
                  <label class="form-check">
                     <input type="checkbox" class="form-check-input" name="fieldc65d35234b8b5f" checked />
                     <span class="form-check-label">Remember me</span>
                  </label>
               </div>
            
            <div class="form-footer">
               <button type="submit" name="submit" class="btn btn-primary w-100" tabindex="3">
                  Sign in
               </button>
            </div>

                     </div>

               </div>
   </form>
               </div>
            </div>

            <div class="text-center text-muted mt-3">
                  <a href="https://glpi-project.org/" title="Powered by Teclib and contributors" class="copyright">GLPI Copyright (C) 2015-2022 Teclib' and contributors</a>
            </div>
         </div>
      </div>
   </div>

   <script type="text/javascript">
   $(function () {
$('#login_name').focus();
});
</script>
</body>
</html>
<div style="background-image: url('/glpi/front/cron.php');"></div></body></html>