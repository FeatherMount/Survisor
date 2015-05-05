import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.scribe.builder.ServiceBuilder;
import org.scribe.model.OAuthRequest;
import org.scribe.model.Response;
import org.scribe.model.Token;
import org.scribe.model.Verb;
import org.scribe.oauth.OAuthService;

/**
 * Accessing the Yelp API V2.
 * Query for restaurant business info in New York.
 * http://www.yelp.com/developers/documentation
 */

public class YelpAPI {

  private static final String API_HOST = "api.yelp.com";
  private static final String DEFAULT_TERM = "restaurant";
  private static final String DEFAULT_LOCATION = "New York";
  private static final int[] NYZIP = {	10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 
	  									10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 
	  									10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 
	  									10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 
	  									10039, 10040, 10044, 10065, 10069, 10075, 10103, 10110, 10111, 
	  									10112, 10115, 10119, 10128, 10152, 10153, 10154, 10162, 10165, 
	  									10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 
	  									10199, 10271, 10278, 10279, 10280, 10282, 10301, 10302, 10303, 
	  									10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 
	  									10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 
	  									10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 
	  									10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 11004, 
	  									11005, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11201, 
	  									11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211, 
	  									11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 
	  									11221, 11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 
	  									11231, 11232, 11233, 11234, 11235, 11236, 11237, 11238, 11239, 
	  									11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 
	  									11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 
	  									11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 
	  									11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 
	  									11420, 11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 
	  									11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 
	  									11692, 11693, 11694, 11697};
  private static final String SEARCH_PATH = "/v2/search";
  private static final String BUSINESS_PATH = "/v2/business";

  /*
   * Update OAuth credentials below from the Yelp Developers API site:
   * http://www.yelp.com/developers/getting_started/api_access
   */
  private static final String CONSUMER_KEY = "sF2V-jbQME2CjkXJjrD-Ng";
  private static final String CONSUMER_SECRET = "E17C7Dz7oLKTQm-XNASeo_k0UOQ";
  private static final String TOKEN = "AMBjqtrnJ3bYawfm4B5T0JkTBw3n-gKg";
  private static final String TOKEN_SECRET = "BV1Ut9yKqcSqi4cn9kvGqQ9a4Pk";

  OAuthService service;
  Token accessToken;
  
  static MongoDB db = new MongoDB();

  /**
   * Setup the Yelp API OAuth credentials.
   * 
   * @param consumerKey Consumer key
   * @param consumerSecret Consumer secret
   * @param token Token
   * @param tokenSecret Token secret
   */
public YelpAPI(String consumerKey, String consumerSecret, String token, String tokenSecret) {
    this.service =
        new ServiceBuilder().provider(TwoStepOAuth.class).apiKey(consumerKey)
            .apiSecret(consumerSecret).build();
    this.accessToken = new Token(token, tokenSecret);
  }

  /**
   * Creates and sends a request to the Search API by term and location.
   * http://www.yelp.com/developers/documentation/v2/search_api
   */
public String searchForBusinessesByLocation(String term, String location, int zip, int offset) {
    OAuthRequest request = createOAuthRequest(SEARCH_PATH);
    request.addQuerystringParameter("term", term);
    request.addQuerystringParameter("location", location + ", " + String.valueOf(zip));
    request.addQuerystringParameter("offset", String.valueOf(offset));
    return sendRequestAndGetResponse(request);
  }

  /**
   * Creates and sends a request to the Business API by business ID.
   * http://www.yelp.com/developers/documentation/v2/business
   */
public String searchByBusinessId(String businessID) {
    OAuthRequest request = createOAuthRequest(BUSINESS_PATH + "/" + businessID);
    return sendRequestAndGetResponse(request);
  }

  /**
   * Creates and returns an {@link OAuthRequest} based on the API endpoint specified.
   */
private OAuthRequest createOAuthRequest(String path) {
    OAuthRequest request = new OAuthRequest(Verb.GET, "http://" + API_HOST + path);
    return request;
  }

  /**
   * Sends an {@link OAuthRequest} and returns the {@link Response} body.
   */
private String sendRequestAndGetResponse(OAuthRequest request) {
//    System.out.println("Querying " + request.getCompleteUrl() + " ...");
    this.service.signRequest(this.accessToken, request);
    Response response = request.send();
    return response.getBody();
  }

  /**
   * Queries the Search API based on the arguments and takes the first result to query
   * the Business API.
   */
  @SuppressWarnings("unchecked")
private static void queryAPI(YelpAPI yelpApi, String term, String location) {
	// get at most 1000 records for each zip code in the location  	
	for (int index = 0; index < NYZIP.length; index++) {
		int zip = NYZIP[index];
		System.out.println("Querying restaurants in zip code " + String.valueOf(zip));
		
		int count = 20;
		int offset = 0;	
		while (count > 0) {
		    String searchResponseJSON = yelpApi.searchForBusinessesByLocation(term, location, zip, offset);

		    JSONParser parser = new JSONParser();
		    JSONObject response = null;
		    try {
		    	response = (JSONObject) parser.parse(searchResponseJSON);
		    	JSONArray businesses = (JSONArray) response.get("businesses");
		    	
		    	if (businesses == null) {
		    		count = 0;
			      	System.out.println(offset);
		    	} else {
		    		count = businesses.size();
		    		offset += count;
		    	}	        

				// get info about each restaurant and write to database
			 	for (int i = 0; i < count; i++) {
			 		JSONObject business = (JSONObject) businesses.get(i);
			 		String businessID = business.get("id").toString();
			 		String businessResponseJSON = yelpApi.searchByBusinessId(businessID.toString());
				        
			 		try {
			 			response = (JSONObject) parser.parse(businessResponseJSON);
			 			JSONObject obj = new JSONObject();
			 			obj.put("name", response.get("name"));
			 			obj.put("rating", response.get("rating"));
			 			if ((JSONObject)response.get("location") != null) {
			 				obj.put("location", ((JSONObject)response.get("location")).get("coordinate"));
			 			}
					  	obj.put("zip", zip);
//					    System.out.println(obj.toJSONString());			        
					  	db.addResToDB(businessID, obj);
			 		} catch (ParseException pe) {
			 			System.out.println("Error: could not parse business JSON response:");
			 			System.out.println(searchResponseJSON);
			 			i = i-1;
			 		}
			 	}
		          
		          
		    } catch (ParseException pe) {
		    	System.out.println("Error: could not parse search JSON response:");
		    	System.out.println(searchResponseJSON);
		    	index = index - 1;
		    }
		        
		}
	}

}

  /**
   * Main entry for sample Yelp API requests.
   */
public static void main(String[] args) {
    YelpAPI yelpApi = new YelpAPI(CONSUMER_KEY, CONSUMER_SECRET, TOKEN, TOKEN_SECRET);
    queryAPI(yelpApi, DEFAULT_TERM, DEFAULT_LOCATION);
  }
}
