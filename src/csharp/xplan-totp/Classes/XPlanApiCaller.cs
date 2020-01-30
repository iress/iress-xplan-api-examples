using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json;

namespace xplan_totp
{
    public class XPlanApiCaller
    { 

        public async Task<List<Client>> GetClientsAsync()
        {
            string baseUrl = "https://xplan.iress.com.au/resourceful/entity/client/";

            string USER = "myusername";
            string PASSWORD = "mypassword";
            string apiID = "myappID";
            string secretKey = "mySecretKey";

            string EncodedAuth = GetAuthHeaderForXPlan(USER, PASSWORD, secretKey);

            using (HttpClient hc = new HttpClient())
            {
                hc.BaseAddress = new Uri(baseUrl);
                hc.DefaultRequestHeaders.Add("Authorization", "Basic " + EncodedAuth);
                hc.DefaultRequestHeaders.Add("X-Xplan-App-Id", apiID);
                
                var result = await hc.GetAsync("?_method=GET");

                result.EnsureSuccessStatusCode();

                string content = await result.Content.ReadAsStringAsync();

                return JsonConvert.DeserializeObject<List<Client>>(content);
            }
        }

        private string GetAuthHeaderForXPlan(string User, string Password, string SecretKey = null)
        {
            string authString = $"{User}:{Password}";

            if (SecretKey != null)
            {
                byte[] decodedKey = Base32.Base32Encoder.Decode(SecretKey);
                OtpSharp.Totp otp = new OtpSharp.Totp(decodedKey);
                string OTP = otp.ComputeTotp();
                authString += $"\n\r\t\a{OTP}";
            }

            var authStringBytes = System.Text.Encoding.UTF8.GetBytes(authString);
            return System.Convert.ToBase64String(authStringBytes);
        }

    }
}
