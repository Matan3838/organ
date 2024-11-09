import streamlit as st
import json

class HomeInventoryApp:
    def __init__(self):
        st.title("Home Inventory Organizer")

        # Data structure to store items
        if 'inventory' not in st.session_state:
            # Load existing data if available
            try:
                with open('home_inventory.json', 'r') as file:
                    st.session_state.inventory = json.load(file)
            except FileNotFoundError:
                st.session_state.inventory = {}

        # Create two columns for layout
        left_col, right_col = st.columns(2)

        with left_col:
            # Area selection
            area = st.selectbox(
                "Area:",
                options=['Living Room', 'Kitchen', 'Bedroom', 'Bathroom', 'Garage']
            )

            # Storage location
            storage = st.selectbox(
                "Storage Location:",
                options=['Closet', 'Drawer', 'Box', 'Shelf', 'Cabinet']
            )

            # Item entry
            item = st.text_input("Item Name:")

            # Add item button
            if st.button("Add Item"):
                self.add_item(area, storage, item)

        with right_col:
            # Display area
            st.subheader("Inventory List")
            if st.session_state.inventory:
                for area in st.session_state.inventory:
                    for storage in st.session_state.inventory[area]:
                        for item in st.session_state.inventory[area][storage]:
                            col1, col2, col3, col4 = st.columns([2,2,2,1])
                            with col1:
                                st.write(area)
                            with col2:
                                st.write(storage)
                            with col3:
                                st.write(item)
                            with col4:
                                if st.button("Delete", key=f"{area}-{storage}-{item}"):
                                    self.delete_item(area, storage, item)

    def add_item(self, area, storage, item):
        if not all([area, storage, item]):
            st.error("Please fill in all fields")
            return

        if area not in st.session_state.inventory:
            st.session_state.inventory[area] = {}
        if storage not in st.session_state.inventory[area]:
            st.session_state.inventory[area][storage] = []
        
        st.session_state.inventory[area][storage].append(item)
        self.save_inventory()
        st.experimental_rerun()

    def delete_item(self, area, storage, item):
        st.session_state.inventory[area][storage].remove(item)
        if not st.session_state.inventory[area][storage]:
            del st.session_state.inventory[area][storage]
        if not st.session_state.inventory[area]:
            del st.session_state.inventory[area]
            
        self.save_inventory()
        st.experimental_rerun()

    def save_inventory(self):
        with open('home_inventory.json', 'w') as file:
            json.dump(st.session_state.inventory, file)

if __name__ == "__main__":
    app = HomeInventoryApp()
