/**
 * Get all reviews by dealer id
 */

 const {CloudantV1} = require('@ibm-cloud/cloudant');
 const {IamAuthenticator} = require('ibm-cloud-sdk-core');
 
 const IAM_API_KEY = "0r2RiQgkweQeJ00QULyiR3NUZyAw-W3cFAZzeGnnExlT";
 const COUCH_URL = "https://1bfe7200-09d7-4b6f-acb5-c3e477ff9b1f-bluemix.cloudantnosqldb.appdomain.cloud";
 const DB_NAME='reviews';
 
 async function main(params) {
    try {

    const authenticator = new IamAuthenticator({apikey: IAM_API_KEY});
     const cloudant = CloudantV1.newInstance({authenticator: authenticator});
     cloudant.setServiceUrl(COUCH_URL);
    
    var dealerId=parseInt(params.dealerId) ;
 
 
         let dbList = await cloudant.postFind({
             db: DB_NAME,
             selector:{'dealership':dealerId}
         });
         return  dbList.result;
 
     } catch (error) {
         return {
             error: error.description
         };
     }
 }