import React from "react";


export default function PlanCard(
	{
		plan,
		handleSubscription,
	}: {
		plan: any,
		handleSubscription: (id: string) => void
	}
) {

	return (
		<>
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
						) : null}
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
						) : null}
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
						) : null}
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
						) : null}
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
						) : null}
						{plan.change_lang ? (
							<li className="flex space-x-3">
								<svg xmlns="http://www.w3.org/2000/svg" className="flex-shrink-0 h-5 w-5 text-green-400"
										 width="24" height="24" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor"
										 fill="none" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
									<path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
									<path d="M5 12l5 5l10 -10"></path>
								</svg>
								<span className="text-base text-slate-700"><strong>10+</strong> languages <i>Danish, Czech, Dutch, English, German, Italian, Japanese, Korean, Polish, Spanish, French</i></span>
							</li>
						) : null}
					</ul>
				</div>
			</div>
		</>
	)
}
