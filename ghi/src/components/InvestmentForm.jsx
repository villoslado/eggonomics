import { useState } from 'react'
import axios from 'axios'

const InvestmentForm = ({ onSubmit }) => {
    const [formData, setFormData] = useState({
        investmentType: '',
        startingValue: '',
        annualWithdrawal: '',
        minYears: '',
        mostLikelyYears: '',
        maxYears: '',
    })

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData({ ...formData, [name]: value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await axios.post(
                'http://localhost:8000/api/calculate-nest-egg/',
                formData
            )
            onSubmit(response.data)
        } catch (error) {
            console.error('Error submitting form:', error)
        }
    }

    return (
        <form onSubmit={handleSubmit} className="investment-form">
            <div className="form-group">
                <label>Investment Type</label>
                <div>
                    {['stocks', 'bonds', 'sb_blend', 'sbc_blend'].map(
                        (type) => (
                            <label key={type}>
                                <input
                                    type="radio"
                                    name="investmentType"
                                    value={type}
                                    checked={formData.investmentType === type}
                                    onChange={handleChange}
                                />
                                {type}
                            </label>
                        )
                    )}
                </div>
            </div>

            <div className="form-group">
                <label>Enter starting value of investment</label>
                <input
                    type="number"
                    name="startingValue"
                    placeholder="10000"
                    value={formData.startingValue}
                    onChange={handleChange}
                />
            </div>

            <div className="form-group">
                <label>Enter annual pre-tax withdrawal (today $)</label>
                <input
                    type="number"
                    name="annualWithdrawal"
                    placeholder="10000"
                    value={formData.annualWithdrawal}
                    onChange={handleChange}
                />
            </div>

            <div className="form-group">
                <label>Enter years in retirement</label>
                <input
                    type="number"
                    name="minYears"
                    placeholder="Minimum (e.g., 10)"
                    value={formData.minYears}
                    onChange={handleChange}
                />
                <input
                    type="number"
                    name="mostLikelyYears"
                    placeholder="Most Likely (e.g., 25)"
                    value={formData.mostLikelyYears}
                    onChange={handleChange}
                />
                <input
                    type="number"
                    name="maxYears"
                    placeholder="Maximum (e.g., 40)"
                    value={formData.maxYears}
                    onChange={handleChange}
                />
            </div>

            <button type="submit" className="submit-button">
                Submit
            </button>
        </form>
    )
}

export default InvestmentForm
