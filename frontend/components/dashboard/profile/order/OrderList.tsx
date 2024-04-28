import OrderCard from "@/components/dashboard/profile/order/OrderCard";
import React from "react";


export default function OrderList(
	{
		orderList
	}:{
		orderList: any[]
	}
){


	return (
		<>
			<div className="w-full max-w-7xl px-4 md:px-5 lg-6 mx-auto">
				<div className="main-box border border-gray-200 rounded-xl pt-6 max-w-xl max-lg:mx-auto lg:max-w-full">
					<div className="w-full px-3 min-[400px]:px-6">

						{Array.isArray(orderList) && (
							orderList.map((order: any) => (
								<OrderCard key={order.id} order={order}/>
							))
						)}
					</div>
				</div>
			</div>
		</>
	)
}