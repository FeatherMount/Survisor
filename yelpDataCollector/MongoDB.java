import java.net.UnknownHostException;

import org.json.simple.JSONObject;

import com.mongodb.BasicDBObject;
import com.mongodb.DB;
import com.mongodb.DBCollection;
import com.mongodb.MongoClient;
import com.mongodb.MongoClientURI;

/*
 * when run in localhost, open mongod in sheel
 * change IP and port if deployed on Amazon aws
 */

public class MongoDB {

	MongoClient mongoClient;
	DB db;
	DBCollection coll;
	String dbName = "survisor";
	String colName = "yelpDB";	
	
	public MongoDB() {
		try {
			String textUri = "mongodb://zhou:cu6998@ds061711.mongolab.com:61711/" + dbName;
			MongoClientURI uri = new MongoClientURI(textUri);
			mongoClient = new MongoClient(uri);	
			db = mongoClient.getDB(dbName);
			coll = db.getCollection(colName);
		} catch (UnknownHostException e) {
			e.printStackTrace();
		}
	}
	
	public void disconnect() {
		System.out.println("Disconnect from database");
		mongoClient.close();
	}
	
	public void addResToDB(String businessId, JSONObject obj) {
		JSONObject point = (JSONObject)obj.get("location");
		if (point != null) {
			BasicDBObject doc = new BasicDBObject("name", obj.get("name"))
	        	.append("rating", obj.get("rating"))
	        	.append("latitude", point.get("latitude"))
	        	.append("longitude", point.get("longitude"))
	        	.append("zip", obj.get("zip"));
			if (coll.find(doc).limit(1).count() == 0) {
				coll.insert(doc);
//				System.out.println("inserting doc into db");
			} else {
//				System.out.println("doc already existed in db");
			}
		}
	}
	
}
