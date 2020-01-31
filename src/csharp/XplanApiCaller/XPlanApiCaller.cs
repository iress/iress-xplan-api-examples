using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Threading.Tasks;

namespace XplanApiCaller
{
    public class XPlanApiCaller
    {
        public async Task<List<Client>> GetClientsAsync(string user, string password, string apiID, string secretKey)
        {
            const string BASE_URL = "https://xplan.iress.com.au/resourceful/entity/client/";

            string EncodedAuth = GetAuthHeaderForXPlan(user, password, secretKey);

            using (HttpClient hc = new HttpClient())
            {
                hc.BaseAddress = new Uri(BASE_URL);
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
#if NETCOREAPP2_0
                byte[] decodedKey = Wiry.Base32.Base32Encoding.Standard.ToBytes(SecretKey);
#else
                byte[] decodedKey = Base32.Base32Encoder.Decode(SecretKey);
#endif
                OtpSharp.Totp otp = new OtpSharp.Totp(decodedKey);
                string OTP = otp.ComputeTotp();
                authString += $"\n\r\t\a{OTP}";
            }

            var authStringBytes = System.Text.Encoding.UTF8.GetBytes(authString);
            return System.Convert.ToBase64String(authStringBytes);
        }

    }
}
