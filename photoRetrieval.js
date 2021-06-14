import nodeFetch from 'node-fetch';
import { createApi } from 'unsplash-js';
import { readFileSync } from 'fs';
import request from 'request';
import AWS from 'aws-sdk';



const env = JSON.parse(readFileSync('./.env.json', 'utf-8'))





function uploadToS3(uri, s3, key) {

  console.log("Attempting to upload photo at " + uri + " to " + key);

  var options = {
    uri: uri,
    encoding: null
  };

  var params = {
    Bucket: env.aws.s3_bucket_name,
    Key: key
  };

  request(options, function(error, response, body) {
      if (error || response.statusCode !== 200) { 
          console.log("Failed to get image at " + options.uri);
          console.log(error);
      } else {
        s3.headObject(params, function (err, metadata) {  
          if (err && err.code === 'NotFound') {  
            s3.putObject({
              Body: body,
              Key: key.toString(),
              Bucket: env.aws.s3_bucket_name
            }, function(error, data) { 
              if (error) {
                console.log("Error uploading image to s3: " + key);
                console.log(error);
              } else {
                console.log("Success uploading to s3: " + key );
              }
            }); 
          } else {
            console.log("File exists in bucket in s3, not uploading " + key);
          }
        });          
      }   
  });
}

const REGION = env.aws.s3_region;
AWS.config.update({region: REGION});
const s3 = new AWS.S3({apiVersion: '2006-03-01'});

const unsplash = createApi({
  accessKey: env.unsplash.access_key,
  fetch: nodeFetch,
});

unsplash.photos.list({}).then(result => {
  if (result.errors) {
    console.log('Error occurred when listing photos from unsplash: ', result.errors[0]);
  } else {
    console.log(`Request status code from listing photot: ${result.status}`);
    
    const photos = result.response.results;
    photos.forEach(photo => {

      const url = photo.urls.raw;
      const key = photo.id + ".jpg";

      uploadToS3(url, s3, key);

    });
  }
});
    