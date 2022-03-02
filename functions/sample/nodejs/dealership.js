function main(params) { 
    
     secret={
        "COUCH_URL": "https://apikey-v2-2gq164uzkyu1fnh02f6jsf23isd0cy97ck6tp4pkujbb:6be8ee03900afeae5d6bd9722666ef06@9f3bee27-06be-4d2f-b424-f4467092fa2f-bluemix.cloudantnosqldb.appdomain.cloud",
        "IAM_API_KEY": "S2RD8A4xkSzlGExm4t83D-axRAXm-FG3rItnyr9rTtgs",
        "COUCH_USERNAME": "apikey-v2-2gq164uzkyu1fnh02f6jsf23isd0cy97ck6tp4pkujbb"
     };

    console.log(params); 

    return new Promise(function (resolve, reject) { 
       const Cloudant = require('@cloudant/cloudant'); 
       const cloudant = Cloudant({ 
           url: secret.COUCH_URL, 
           plugins: {iamauth: {iamApiKey:secret.IAM_API_KEY}} 
       }); 

         const dealershipDb = cloudant.use('dealerships'); 
    
         if (params.state) { 
               // return dealership with this state 
               dealershipDb.find({"selector": {"state": {"$eq": params.state}}}, function(err, result) { 
                   if (err) { 
                       console.log("🚀 ~ file: index.js ~ line 20 ~ err", err) 
                       reject(err); 
                   } 
                   let code=200; 
                   if (result.docs.length==0) 
                   { 
                        code= 404; 
                   } 
                   resolve({ 
                       statusCode: code, 
                       headers: { 'Content-Type': 'application/json' }, 
                       body: result 
                   }); 
               }); 
         } else if (params.id) { 
           id=parseInt(params.dealerId) 
           dealershipDb.find({selector: {id:parseInt(params.id)}}, function (err, result) { 
               if (err) { 
                   console.log("🚀 ~ file: ind ex.js ~ line 20 ~ err", err) 
                   reject(err); 
               } 
               let code=200; 
                   if (result.docs.length==0) 
                   { 
                   code= 404; 
                   } 
    	 resolve({ 
                   statusCode: code, 
                   headers: { 'Content-Type': 'application/json' }, 
                   body: result 
               }); 
           }); 
        } else { 
         // return all documents 
            dealershipDb.list({ include_docs: true }, function (err, result) { 
               if (err) { 
                   console.log("🚀 ~ file: index.js ~ line 35 ~ err", err) 
                   reject(err); 
               } 
                resolve({ 
                   statusCode: 200, 
                   headers: { 'Content-Type': 'application/json' }, 
                   body: result 
                }); 
           }); 
        } 
    }); 
} 
    
