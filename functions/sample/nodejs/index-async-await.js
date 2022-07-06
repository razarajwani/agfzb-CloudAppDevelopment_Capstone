/**
 * Get all dealerships
 */

 const { CloudantV1 } = require('@ibm-cloud/cloudant');
 const { IamAuthenticator } = require('ibm-cloud-sdk-core');
 
 async function main(params) {
       const authenticator = new IamAuthenticator({ apikey: "0r2RiQgkweQeJ00QULyiR3NUZyAw-W3cFAZzeGnnExlT" })
       const cloudant = CloudantV1.newInstance({
           authenticator: authenticator
       });
       cloudant.setServiceUrl("https://1bfe7200-09d7-4b6f-acb5-c3e477ff9b1f-bluemix.cloudantnosqldb.appdomain.cloud");
       
       try {
         let dbList = await cloudant.getAllDbs();
         return { "dbs": dbList.result };
       } catch (error) {
           return { error: error.description };
       }
 }
 
 
 
 