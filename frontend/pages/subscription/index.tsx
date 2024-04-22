import {useSession} from "next-auth/react";
import Layout from "@/components/Layout";
import {useEffect, useState} from "react";
import {toast} from "react-toastify";

async function getPlans(){
	const res = await fetch(process.env.API_URL + "subscription/plan/", {
		method: "get",
	})
	return await res.json();
}


export default function Home() {
	const {data: session, status} = useSession({required: false});
	const [plans, setPlans] = useState([]);

	useEffect(() => {
		async function fetchData(){
			const data = await getPlans();
			setPlans(data);
		}

		fetchData();
	}, []);


	const handleSubscription = async (planId: string) => {
		if (!session){
			toast.error("Please login to continue")
			return;
		}

		try {
			const response = await fetch('http://localhost:8000/api/subscription/checkout/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${session?.access_token}`
				},
				body: JSON.stringify({
					plan_id: planId
				})
			});
			if (response.ok) {
				const data = await response.json();
				console.log(data)

				window.location.href = data;
			} else {
				toast.error(response.text)
			}
		} catch (error) {
			toast.error("Error")
		}
	};

	return (
		<>
			<Layout>
				<main>
					{
						<div
							className="mt-12 space-y-3 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-3 sm:gap-6 md:max-w-5xl md:mx-auto xl:grid-cols-3">
							{Array.isArray(plans) && (
								plans.map((plan) => (
									<div key={plan.id} className="border border-slate-200 rounded-lg shadow-sm divide-y divide-slate-200">
										<div className="p-6">
											<h2 className="text-xl leading-6 font-bold text-slate-900">{plan?.name}</h2>
											<p className="mt-2 text-base text-slate-700 leading-tight">{plan?.description}</p>
											<p className="mt-8">
												<span className="text-4xl font-bold text-slate-900 tracking-tighter">$ {plan?.price.price}</span>
												<span className="text-base font-medium text-slate-500">/mo</span>
											</p>
											<button onClick={() => handleSubscription(plan.id)}
															className="text-white mt-5 bg-blue-500 hover:bg-blue-600 font-semibold rounded-md text-sm px-4 py-3 w-full">
												Subscribe
											</button>
										</div>
										<div className="pt-6 pb-8 px-6">
											<h3 className="text-sm font-bold text-slate-900 tracking-wide uppercase">Whats included</h3>
											<ul role="list" className="mt-4 space-y-3">
												{plan.youtube ? (
													<li className="flex space-x-3">
														<svg xmlns="http://www.w3.org/2000/svg" className="flex-shrink-0 h-5 w-5 text-green-400"
																 width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"
																 fill="none" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
															<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
															<path d="M5 12l5 5l10 -10"></path>
														</svg>
														<span className="text-base text-slate-700">Youtube</span>
													</li>
												): null}
												{plan.spotify ? (
													<li className="flex space-x-3">
														<svg xmlns="http://www.w3.org/2000/svg" className="flex-shrink-0 h-5 w-5 text-green-400"
																 width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"
																 fill="none" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
															<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
															<path d="M5 12l5 5l10 -10"></path>
														</svg>
														<span className="text-base text-slate-700">Spotify</span>
													</li>
												): null}
												{plan.max_length ? (
													<li className="flex space-x-3">
														<svg xmlns="http://www.w3.org/2000/svg" className="flex-shrink-0 h-5 w-5 text-green-400"
																 width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"
																 fill="none" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
															<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
															<path d="M5 12l5 5l10 -10"></path>
														</svg>
														<span className="text-base text-slate-700"><strong>{plan.max_length}</strong> minutes</span>
													</li>
												): null}
												{plan.max_result ? (
													<li className="flex space-x-3">
														<svg xmlns="http://www.w3.org/2000/svg" className="flex-shrink-0 h-5 w-5 text-green-400"
																 width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"
																 fill="none" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
															<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
															<path d="M5 12l5 5l10 -10"></path>
														</svg>
														<span className="text-base text-slate-700"><strong>{plan.max_result}</strong> results</span>
													</li>
												): null}
												{plan.duration ? (
													<li className="flex space-x-3">
														<svg xmlns="http://www.w3.org/2000/svg" className="flex-shrink-0 h-5 w-5 text-green-400"
																 width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"
																 fill="none" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
															<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
															<path d="M5 12l5 5l10 -10"></path>
														</svg>
														<span className="text-base text-slate-700"><strong>{plan.duration}</strong> days</span>
													</li>
												): null}
											</ul>
										</div>
									</div>
								))
							)}
						</div>

					}
				</main>
			</Layout>
		</>
	);
}