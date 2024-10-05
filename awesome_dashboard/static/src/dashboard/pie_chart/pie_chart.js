/** @odoo-module */

import { loadJS } from "@web/core/assets";
import { getColor } from "@web/core/colors/colors";
import { Component, onWillStart, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class PieChart extends Component {
    static template = "awesome_dashboard.PieChart";
    static props = {
        label: String,
        data: Object,
    };

    setup() {
        this.actionService = useService("action");
        this.canvasRef = useRef("canvas");
        onWillStart(() => loadJS(["/web/static/lib/Chart/Chart.js"]));
        onMounted(() => {
            this.renderChart();
        });
        onWillUnmount(() => {
            this.chart.destroy();
        });
    }

    renderChart() {
        const labels = Object.keys(this.props.data);
        const data = Object.values(this.props.data);
        const color = labels.map((_, index) => getColor(index));
        this.chart = new Chart(this.canvasRef.el, {
            type: "pie",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: this.props.label,
                        data: data,
                        backgroundColor: color,
                    },
                ],
            },
            options: {
                onClick: (e) => {
                    const active = e.chart.getActiveElements();
                    if (active) {
                        const sizeLabel = e.chart.data.labels[active[0].index];

                        // Логирование для отладки
                        console.log('sizeLabel:', sizeLabel);
                        if (sizeLabel) {
                            this.actionService.doAction({
                                name: "Orders for Size: " + sizeLabel,
                                type: "ir.actions.act_window",
                                res_model: "sale.order",
                                views: [
                                    [false, "list"],
                                    [false, "form"],
                                ],
                                domain: [["size", "=", sizeLabel]],
                            });
                        }
                    }
                }
            }
        });
    }
}