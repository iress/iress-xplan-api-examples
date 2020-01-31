using System;
using System.Linq;
using XplanApiCaller;

namespace xplan_totp
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                const string USER = "testuser";
                const string PASSWORD = "ASDDsf3sdsf2";
                const string API_ID = "FPj9cymketaHXunJE3E3";
                const string SECRET_KEY = "HTHHH72MQ7CBVX3SU25YRKQO6OAI36TD";

                XPlanApiCaller apiCaller = new XPlanApiCaller();
                var clients = apiCaller.GetClientsAsync(USER, PASSWORD, API_ID, SECRET_KEY).Result;

                foreach (var client in clients.Take(10))
                    Console.WriteLine($"{client.id} - {client.entity_name}");
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
            }

            Console.WriteLine("Press any key to continue...");
            Console.ReadLine();
        }
    }
}
