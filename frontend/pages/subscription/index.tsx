import {useSession} from "next-auth/react";

export default function Home() {
  const {data: session, status} = useSession({required: true});

const handleSubscription = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/subscription/checkout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session?.access_token}`
        },
        body: JSON.stringify({
          price_id: 'price_1P6vSVE3z5SG6L41bej8QhXE'
        })
      });
      if (response.ok) {
        const data = await response.json();
        console.log(data)

        window.location.href = data;
      } else {
        console.error(response.statusText);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <h1>Subscription</h1>
      <div className='subscription'>
        <div className='starter-div'>
          <h2>Starter plan</h2>
          <button className="btn-month" onClick={handleSubscription}>&#8377;30 / Month</button>
        </div>
      </div>
      <br />
    </>
  );
}