/**
 * Submit Reviews
 */

 const {CloudantV1} = require('@ibm-cloud/cloudant');
 const {IamAuthenticator} = require('ibm-cloud-sdk-core');
 
 const IAM_API_KEY = "0r2RiQgkweQeJ00QULyiR3NUZyAw-W3cFAZzeGnnExlT";
 const COUCH_URL = "https://1bfe7200-09d7-4b6f-acb5-c3e477ff9b1f-bluemix.cloudantnosqldb.appdomain.cloud";
 const DB_NAME='reviews';
 
 async function main(params) {
     const authenticator = new IamAuthenticator({apikey: IAM_API_KEY});
     const cloudant = CloudantV1.newInstance({authenticator: authenticator});
     cloudant.setServiceUrl(COUCH_URL);
    
     try {
  
       let req = await cloudant.postDocument({
             db: DB_NAME,
             document: params
         });
         return  req.result;
 
     } catch (error) {
         return {
             error: error.description
         };
     }
 }