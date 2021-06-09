import nodeFetch from 'node-fetch';
import { createApi } from 'unsplash-js';
import { createWriteStream, existsSync, readFileSync} from 'fs';
import request from 'request';

const env = JSON.parse(readFileSync('./.env.json', 'utf-8'))

const unsplash = createApi({
    accessKey: env.unsplash.access_key,
    fetch: nodeFetch,
});

var download = function(uri, filename, callback) {
  request.head(uri, function(err, res, body){
    request(uri).pipe(createWriteStream(filename)).on('close', callback);
  });
};

unsplash.photos.list({}).then(result => {
  if (result.errors) {
    console.log('error occurred: ', result.errors[0]);
  } else {
    console.log(`Request status code: ${result.status}`);
    
    const photos = result.response.results;
    photos.forEach(photo => {
      var filePath = './images/' + photo.id +'.jpg';
      if (!existsSync(filePath)) {
        download(photo.urls.raw, filePath, function(){
          console.log(`Downloaded file to ${filePath}`);
        });
      } else {
        console.log("Image has already been downloaded");
      }
    });
  }
});
    
