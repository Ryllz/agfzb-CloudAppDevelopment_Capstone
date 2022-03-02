/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');

 async function main(params) {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
 
     try {
         let dbList = await cloudant.db.list();
         return { "dbs": dbList };
     } catch (error) {
         return { error: error.description };
     }
 
 }

 let databases = cloudant.db.list();
 let dealerships_db = cloudant.db.use("dealerships");
 let reviews_db = cloudant.db.use("reviews");

 async function action_get_all_dealerships(dealerships_db) {
    try {
        let all_dealerships = await get_database(dealerships_db);
        let result = {};
        all_dealerships.forEach((item) => {
        result[item.id] = item;
        });
        return { json_dealerships: JSON.stringify(result) };
    } catch (error) {
        return { error: error.description };
    }
 }