// Server side code

export async function POST(request) {
    try {
        const { fileBuffer, fileType, width, height } = await request.json();

        if (!fileBuffer || !width || !height) {
            return NextResponse.json({ message: 'Missing required fields' }, { status: 400 });
        }

        const croppedImageBuffer = await sharp(Buffer.from(fileBuffer, 'base64'))
            .resize(parseInt(width), parseInt(height))
            .toBuffer();

        console.log("post method message", croppedImageBuffer)
        return new NextResponse(croppedImageBuffer, {
            headers: {
                'Content-Type': fileType,  // Set correct content type (e.g., 'image/jpeg')
            }
            })
    } catch (error) {
        console.error('Error processing image:', error);
        return NextResponse.json({ message: 'Internal Server Error' }, { status: 500 });
    }
}


//client side code
async function uploadFile(file, fileType, folder, toastMessage, data) {
    if (!(file instanceof FileList)) {
      return;
    }

  try {
      const signedUrlResponse = await axios.get(
        `${
          process.env.API_URI
        }/movies/s3/signed-url?fileName=${data.title.toLowerCase().replaceAll(" ", "_")}.${
          file[0].type.split("/")[1]
        }&type=${fileType}&folder=${folder}`,
        {
          headers: {
            Authorization: session.data.user.token,
          },
        }
        
      );

  const signedUrl = signedUrlResponse.data.url;

      toast("Uploading");

      if(fileType === "poster"){
        // Wrap FileReader in a promise
        const readFile = (file) => {
          return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsArrayBuffer(file);
          });
        };

    try {
       // Wait for the file to be read
            const arrayBuffer = await readFile(file[0]);

            // Convert ArrayBuffer to base64
            const base64File = Buffer.from(arrayBuffer).toString('base64');


            // Send the file to your API route for processing
            const response = await axios.post('/api/resize-image', {
              fileBuffer: base64File,
              fileType: file[0].type,
              width: 400,
              height: 500,
            }, {
              responseType: 'arraybuffer',  // Ensure we get binary data as a response
            });

        // Processed image in base64 format
            const processedImage = response.data;
            // Convert base64 back to binary to upload to S3
            //const processedImageBuffer = Buffer.from(processedImage, 'base64');

            // Create a Blob from the binary data
            const blob = new Blob([response.data], { type: file[0].type });

            // Create a new File object using the Blob
            const processedImageFile = new File([blob], file[0].name, {
              type: file[0].type,
            });

            await axios.put(signedUrl, processedImageFile, {
              headers: {
                "Content-Type": file[0].type,
              },
            });
            console.log("Processed Image:", processedImage, processedImageFile, file[0]);
          } catch (error) {
            console.error('Error uploading file:', error);
          }


          }
      else{
        await axios.put(signedUrl, file[0], {
          headers: {
            "Content-Type": file[0].type,
          },
        });
      }

      toast.success(toastMessage);

      return `https://movie-poster-and-trailers.s3.eu-west-2.amazonaws.com/${data.title.toLowerCase().replaceAll(
        " ",
        "_"
      )}/${fileType}/${data.title.toLowerCase().replaceAll(" ", "_")}.${
        file[0].type.split("/")[1]
      }`;
    } catch (error) {
      console.log(error);
      if (error.response) {
        toast.error(error.response.data.message);
      }
    }
  }
