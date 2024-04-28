import PlanCard from "@/components/subscription/PlanCard";
import React from "react";


export default function PlanList(
	{
		plans,
		handleSubscription,
	}: {
		plans: any,
		handleSubscription: (id: string) => void
	}
) {

	return (
		<>
			<div
				className="mt-12 space-y-3 sm:mt-16 sm:space-y-0 sm:grid sm:grid-cols-3 sm:gap-6 md:max-w-5xl md:mx-auto xl:grid-cols-3"
			>
				{Array.isArray(plans) && (
					plans.map((plan: any) => (
						<PlanCard key={plan?.id} plan={plan} handleSubscription={handleSubscription}/>
					))
				)}
			</div>
		</>
	)
}