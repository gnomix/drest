
ChangeLog
==============================================================================

All bugs/feature details can be found at: 

   https://github.com/derks/drest/issues/XXXXX


Where XXXXX is the 'Issue #' referenced below.  Additionally, this change log
is available online at:

    http://drest.readthedocs.org/en/latest/changelog.html

.. raw:: html

    <BR><BR>

0.9.5 - development (will be released as 0.9.6)
------------------------------------------------------------------------------

Bug Fixes:

    - None
 
Feature Enhancements:

    - None
    
Incompatible Changes:

    - None
    

0.9.4 - Feb 16, 2012
------------------------------------------------------------------------------

Bug Fixes:

    - :issue:`3` - TypeError: object.__init__() takes no parameters
 
Feature Enhancements:

    - Improved test suite, now powered by Django TastyPie!
    - Added support for Basic HTTP Auth.
    
Incompatible Changes:

    - drest.api.API.auth() now implements Basic HTTP Auth by default rather
      than just appending the user/password/etc to the URL.
    
    
.. raw:: html

    <BR><BR>
    
0.9.2 - Feb 01, 2012
------------------------------------------------------------------------------

    - Initial Beta release.  Future versions will detail bugs/features/etc.