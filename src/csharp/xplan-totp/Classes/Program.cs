using System;
using System.Linq;
using System.Net.Http.Headers;
using System.Text;

namespace xplan_totp
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                XPlanApiCaller apiCaller = new XPlanApiCaller();
                var clients = apiCaller.GetClientsAsync().Result;

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
