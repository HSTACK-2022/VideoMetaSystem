function zip_download_content( zip, entryName, filename )
{
	zip.file( entryName ).async("base64").then(
		function ( base64Text )
		{
			download("data:application/octet-stream;base64," + base64Text, filename, "application/octet-stream");		
		}
	);
}

function zip_ext_image_to_tag( zip, entryName, imgTagId )
{
	zip.file( entryName ).async("base64").then(
		function ( base64Text )
		{
			var img = document.getElementById( imgTagId );
			img.setAttribute( 'src', 'data:image/jpeg;base64, ' + base64Text );
		}
	);
}
